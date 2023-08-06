import numpy as np
from numpy import linalg as la

from . import CheckerboardLattice

class ExtendedBasisLattice(CheckerboardLattice.CheckerboardLattice):

    def __init__(self, Vtot, Ratio, n_plane_waves, Frequency, K0, nFloquetBasis, Ellipse_Factor=1):

        super().__init__(Vtot, Ratio, n_plane_waves)
        self.Frequency = Frequency
        # Coupling strength for circles needs to be adjusted by 1+i since there is a relative phase between x and y
        self.CouplingStrength = K0*self.Er/np.pi
        self.nFloquetBasis = nFloquetBasis
        self.n_freq = 2 * nFloquetBasis + 1
        self.Ellipse_Factor = Ellipse_Factor

    def DiagonalizeExtendedBasis_qx(self, q_points, n_to_keep=25, qy=0):

        self.qx = np.linspace(-1, 1, q_points)
        self.ExtendedEnergies = np.zeros((q_points, n_to_keep))  # Full size = self.n_freq * self.plane_wave_dim_2d))

        for loop, kx in enumerate(self.qx):
            self.Hd = ((-2 * self.n_plane_waves + np.mod(self.idx - 1, self.plane_wave_dim_1d) + np.floor(
                (self.idx - 1) / self.plane_wave_dim_1d) + kx) ** 2 +
                       (np.mod(self.idx - 1, self.plane_wave_dim_1d) - np.floor(
                           (self.idx - 1) / self.plane_wave_dim_1d) + qy) ** 2
                       )

            self.H0 = self.Hod + (self.Er * np.diag(self.Hd))
            self.SetUpExtendedBasis(kx, qy)

            self.ExtendedEnergies[loop, :] = np.sort(la.eigvalsh(self.H_extended))[:n_to_keep]

    def DiagonalizeExtendedBasis_GMKG(self, n_per_line, n_to_keep=25, to_numpy=True):
        """
        Diagonalize in the extened basis along the Gamma->M->K->Gamma Line.  In coordinates, it is
        (0,0)->(1,0) ->(0,1)->(0,0)
    
        Parameters:
        n_per_line: int
          Number of points to consider along each line section.  Total number of diagonalizations will be this x3.
        """

        # (0,0) -> (1,0)
        qx1 = np.linspace(0, 1, n_per_line)
        qy1 = 0 * qx1

        # (1,0) -> (1/2,1/2)
        qx2 = np.linspace(1, 1 / 2, n_per_line // 2)
        qy2 = np.linspace(0, 1 / 2, n_per_line // 2)

        # (1/2,1/2) -> (0,0)
        qy3 = np.linspace(1 / 2, 0, n_per_line // 2)
        qx3 = 1 * qy3

        self.qx = np.concatenate([qx1, qx2, qx3])
        self.qy = np.concatenate([qy1, qy2, qy3])

        self.ExtendedEnergies = np.zeros((len(self.qx), n_to_keep))

        for loop, (kx, ky) in enumerate(zip(self.qx, self.qy)):
            self.ExtendedEnergies[loop, :] = self.DiagonalizePoint(kx, ky, n_to_keep, to_numpy)

    def DiagonalizePoint(self, qx, qy, n_to_keep=25, to_numpy=True):
        self.Hd = ((-2 * self.n_plane_waves + np.mod(self.idx - 1, self.plane_wave_dim_1d) + np.floor(
            (self.idx - 1) / self.plane_wave_dim_1d) + qx) ** 2 +
                   (np.mod(self.idx - 1, self.plane_wave_dim_1d) - np.floor(
                       (self.idx - 1) / self.plane_wave_dim_1d) + qy) ** 2
                   )
        self.H0 = self.Hod + (self.Er * np.diag(self.Hd))
        self.SetUpExtendedBasis(qx, qy)
        if to_numpy:
            return np.sort(la.eigvalsh(self.H_extended)).get()[:n_to_keep]
        else:
            return np.sort(la.eigvalsh(self.H_extended))[:n_to_keep]

    def SetUpExtendedBasis(self, qx, qy):
        """
        Generate the Hamiltonian in the extended basis.  Given the static Hamiltonian H0, this matrix is 
    
        | H0 - w  | H1  | 0     | ... |
        |______________________________
        | H-1     | H0  | H1    | ... |
        |_____________________________
        |0        | H-1 | H0 + w| H1..|
    
        This is a tri-block diagonal matrix where the diagonal blocks are Ho - nw I and the 
        off diagonal blocks H1/H-1 are the +/- 1 fourier components.  Since we only consider a 
        single frequency, we only have H1 = CouplingStrength*momentum (which will be diaoonal).  The coupling strength
        is technically Shake_x + Shake_y, so for a circular shake, the coupling needs 
        to be adjusted by 1j in a direction to account for the phase.  
        """

        self.floquet_freq = np.arange(-self.nFloquetBasis, self.nFloquetBasis + 1)

        # Generate the diagonal H0 - nwI.  The full H0 diagonal block will just be 
        # np.kron( H0, np.eye(2*nFloquet+1)) which repeats H0 along the diagonal 2*nFloquet+1 times
        self.Hd = np.kron(np.eye(2 * self.nFloquetBasis + 1), self.H0)

        # This will add -nw to the diagonal components
        self.H0_nomega = self.Frequency * np.kron(np.diag(self.floquet_freq), np.eye(self.H0.shape[0]))

        self.Hdiag = self.Hd + self.H0_nomega

        # Generate H1 and H-1 which will just be coupling_strength*momentum, where momentum will be the q+n*k plane wave component
        # I am making the qy component imaginary to account for circular shaking

        self.CouplingMatrix = np.diag(self.CouplingStrength * ((-2 * self.n_plane_waves + np.mod(self.idx - 1,
                                                                                                 self.plane_wave_dim_1d) + np.floor(
            (self.idx - 1) / self.plane_wave_dim_1d) + qx) +
                                                               (np.mod(self.idx - 1, self.plane_wave_dim_1d) - np.floor(
                                                                   (
                                                                               self.idx - 1) / self.plane_wave_dim_1d) + qy) * 1j * self.Ellipse_Factor
                                                               ))
        # This is a (2n+1)^2 x (2n+1)^2 block  It needs to be along the +1 and -1 diagonal
        self.H1 = np.kron(np.diag(np.ones(2 * self.nFloquetBasis), 1), self.CouplingMatrix) + np.conj(
            np.kron(np.diag(np.ones(2 * self.nFloquetBasis), -1), self.CouplingMatrix))
        self.H_extended = (self.Hdiag + self.H1)