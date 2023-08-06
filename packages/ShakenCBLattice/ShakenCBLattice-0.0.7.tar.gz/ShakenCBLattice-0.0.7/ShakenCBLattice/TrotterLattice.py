import numpy as np
from numpy import linalg as la

from . import CheckerboardLattice


class TrotterLattice(CheckerboardLattice.CheckerboardLattice):
    def __init__(self, Vtot, Ratio, n_plane_waves):
        super().__init__(Vtot, Ratio, n_plane_waves)
        self.GenerateOffDiagonal()

    def shake(self, kx, ky, Omega, K0, N_trotter, phase=np.pi / 2, dx=None, dy=None):
        """
        Get Shaken Eigenvalues for given (kx,ky).  Result stored
        in self.Floquet_E
        """
        self.Omega = Omega
        self.K0 = K0
        self.Period_ = 2 * np.pi / self.Omega
        self.NT_ = N_trotter
        self.phase = phase
        self.times_ = np.linspace(0, self.Period_, self.NT_)
        self.dt = self.times_[2] - self.times_[1]
        Amp = 2 / 7.5 * K0 / (0.54 * Omega * 10 ** (-3))

        if dx:
            self.dx = dx
        else:
            self.dx = Amp * np.pi / 0.406
        if dy:
            self.dy = dy
        else:
            self.dy = 1 * self.dx

        self.Hd = (
            -2 * self.n_plane_waves
            + np.mod(self.idx - 1, self.plane_wave_dim_1d)
            + np.floor((self.idx - 1) / self.plane_wave_dim_1d)
            + kx
        ) ** 2 + (
            np.mod(self.idx - 1, self.plane_wave_dim_1d)
            - np.floor((self.idx - 1) / self.plane_wave_dim_1d)
            + ky
        ) ** 2

        self.H = self.Hod + (self.Er * np.diag(self.Hd))

        static_energies, static_vectors = la.eigh(self.H)
        static_vectors = static_vectors[:, np.argsort(static_energies)]
        static_energies = np.sort(static_energies)
        BlochBasis = np.diag(np.exp(-1j * static_energies * self.dt))
        FourierBasis = np.matmul(
            static_vectors, np.matmul(BlochBasis, np.transpose(static_vectors))
        )
        # Trotter Matrix
        TrotterMat = np.eye(self.dim ** 2, dtype=np.complex)

        for t in self.times_:
            DiagonalTM = np.exp(
                1j
                / 2
                * self.dt
                * self.Omega
                * (
                    self.dx
                    * (cos(self.Omega * t))
                    * (
                        -self.ol_dim * self.n_cut
                        + np.mod(self.idx - 1, self.dim)
                        + np.floor((self.idx - 1) / self.dim)
                        + kx
                    )
                    + self.dy
                    * (cos(self.Omega * t + self.phase))
                    * (
                        np.mod(self.idx - 1, self.dim)
                        - np.floor((self.idx - 1) / self.dim)
                        + ky
                    )
                )
            )
            dTM = np.diag(DiagonalTM)
            TrotterMat = np.matmul(
                dTM, np.matmul(FourierBasis, np.matmul(dTM, TrotterMat))
            )
            shakeEigs, ShakeVecs = la.eig(TrotterMat)
            vecs_dot_static = np.abs(np.dot(np.transpose(ShakeVecs), static_vectors))
            max_idx = np.argmax(vecs_dot_static, axis=0)
            if max_idx[0] == max_idx[1]:
                max_idx[1] = np.argsort(vecs_dot_static[:, 1])[-2]
            SortedShaking = shakeEigs[max_idx]
            self.Floquet_E = np.real(1j * np.log(SortedShaking)) / self.Period_
