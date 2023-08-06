import numpy as np
from numpy import linalg as la


class CheckerboardLattice:
    Er = 3478

    def __init__(self, Vtot, Ratio, n_plane_waves):

        self.Vtot = Vtot
        self.Ratio = Ratio
        self.V2D = Vtot * Ratio * self.Er
        self.Vop = Vtot * (1 - Ratio) * self.Er
        self.Vz = self.Vop
        self.n_plane_waves = n_plane_waves
        self.plane_wave_dim_1d = 2 * n_plane_waves + 1
        self.plane_wave_dim_2d = (2 * n_plane_waves + 1) ** 2

        self.couplings = {
            "A": -self.V2D / 8 - self.Vop / 16,
            "B": -self.Vop / 8,
            "C": np.conj(-self.V2D / 8 - self.Vop / 16),
            "D": np.conj(-self.Vop / 8),
        }
        self.GenerateOffDiagonal()
        self.res = self.q0_gaps([(0, 1)])[0]

    def GenerateOffDiagonal(self):
        A = self.couplings["A"]
        B = self.couplings["B"]
        C = self.couplings["C"]
        D = self.couplings["D"]
        dim = self.plane_wave_dim_1d
        idx = np.linspace(1, dim ** 2, dim ** 2)
        self.idx = idx
        C1 = B * np.ones((1, dim ** 2 - 1)) * (np.mod(idx[0 : dim ** 2 - 1], dim) > 0)
        Cm1 = D * np.ones((1, dim ** 2 - 1)) * (np.mod(idx[0 : dim ** 2 - 1], dim) > 0)
        C2 = (
            A
            * np.ones((1, dim ** 2 - (dim + 1)))
            * (np.mod(idx[0 : dim ** 2 - (dim + 1)], dim) > 0)
        )
        Cm2 = (
            C
            * np.ones((1, dim ** 2 - (dim + 1)))
            * (np.mod(idx[0 : dim ** 2 - (dim + 1)], dim) > 0)
        )
        C3 = B * np.ones((1, dim ** 2 - dim))
        Cm3 = D * np.ones((1, dim ** 2 - dim))
        C4 = (
            A
            * np.ones((1, dim ** 2 - (dim - 1)))
            * (np.mod(idx[0 : dim ** 2 - (dim - 1)], dim) > 0)
        )
        Cm4 = (
            C
            * np.ones((1, dim ** 2 - (dim - 1)))
            * (np.mod(idx[0 : dim ** 2 - (dim - 1)] - 1, dim) > 0)
        )
        self.Hod = (
            np.diag((C1[0]), 1)
            + np.diag(Cm1[0], -1)
            + np.diag(C2[0], dim + 1)
            + np.diag(Cm2[0], -dim - 1)
            + np.diag(C3[0], dim)
            + np.diag(Cm3[0], -dim)
            + np.diag(C4[0], dim - 1)
            + np.diag(Cm4[0], -(dim - 1))
        )

    def diagonalize_qx(self, q_points, qy=0):
        self.qx = np.linspace(-1, 1, q_points)
        self.StaticEnergies = np.zeros((q_points, self.plane_wave_dim_2d))
        for loop, kx in enumerate(self.qx):
            self.Hd = (
                -2 * self.n_plane_waves
                + np.mod(self.idx - 1, self.plane_wave_dim_1d)
                + np.floor((self.idx - 1) / self.plane_wave_dim_1d)
                + kx
            ) ** 2 + (
                np.mod(self.idx - 1, self.plane_wave_dim_1d)
                - np.floor((self.idx - 1) / self.plane_wave_dim_1d)
                + qy
            ) ** 2

            self.H = self.Hod + (self.Er * np.diag(self.Hd))
            self.StaticEnergies[loop, :] = np.sort(la.eigvalsh(self.H))

    def diagonalize_q(self, qx, qy, N_energies=2):
        self.Hd = (
            -2 * self.n_plane_waves
            + np.mod(self.idx - 1, self.plane_wave_dim_1d)
            + np.floor((self.idx - 1) / self.plane_wave_dim_1d)
            + qx
        ) ** 2 + (
            np.mod(self.idx - 1, self.plane_wave_dim_1d)
            - np.floor((self.idx - 1) / self.plane_wave_dim_1d)
            + qy
        ) ** 2
        self.H = self.Hod + (self.Er * np.diag(self.Hd))
        return np.sort(la.eigvalsh(self.H))[:N_energies]

    def q0_gaps(self, band_indexes):
        """
        Get q = 0 gap between given band indices.   band_indexes should be a list of tuples
        containing (low band, high band), so band_indexes = (0,1) gives the difference between
        lowest 2 bands
        """
        n_to_get = np.max(band_indexes) + 1
        Energies = self.diagonalize_q(0, 0, n_to_get)
        energies = []
        for transitions in band_indexes:
            energies.append(Energies[transitions[1]] - Energies[transitions[0]])
        return energies
