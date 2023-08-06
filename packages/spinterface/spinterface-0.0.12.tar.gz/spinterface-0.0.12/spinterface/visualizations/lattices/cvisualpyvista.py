# -*- coding: utf-8 -*-
r"""
Module contains implementation of pyvista visualizations for spin lattices.
"""
from pathlib import Path
from spinterface.visualizations.lattices.utilities import get_colormap
import pyvista as pv
import numpy as np
from spinterface.visualizations.lattices.ivisualizer import IVisualizer
from spinterface.inputs.lattice.ILattice import ILattice
from typing import List, Tuple, Union
from spinterface.visualizations.const import SPINDEFAULT_SETTINGS, EVECDEFAULT_SETTINGS
from spinterface.inputs.lattice.const import LATT_TYPE_EVEC, LATT_TYPE_SPIN


class CVisualPyVista(IVisualizer):
    r"""
    Class for visualizing spin lattices with py vista library
    """

    def __init__(self, lattice: ILattice, tiplength: Union[float, None] = None, tipradius: Union[float, None] = None,
                 arrowscale: Union[float, None] = None, draw_background: Union[bool, None] = None,
                 cam: Union[List[Tuple[float, float, float]], None] = None,
                 cmap: str = 'hsv_spind', stat_moms: bool = False, stat_mom_nr: int = 2, total_mag=False) -> None:
        r"""
        Initializes the visualization

        Args:
            tiplength(float): geometry of arrow: tiplength
            tipradius(float): geometry of arrow: tipradius
            arrowscale(float): geometry of arrow: arrowscale
            draw_background(bool): shall i draw the background of the lattice
            camera: camera position
            cmap: string for the choice of the colormap. Defined in utilities module
            stat_moms(bool): present the statistical moments of the lattice
            stat_mom_nr(int): number of statistical moments to present
        """
        super().__init__(lattice)
        self.stat_moms = stat_moms
        self.stat_mom_nr = stat_mom_nr
        self.total_mag = total_mag
        self.tiplength, self.tipradius, self.arrowscale, self.drawbackground = self._load_settings(tiplength, tipradius,
                                                                                                   arrowscale,
                                                                                                   draw_background)
        self._geom = pv.Arrow(start=np.array([-self.arrowscale / 2.0, 0, 0]), tip_length=self.tiplength,
                              tip_radius=self.tipradius, scale=self.arrowscale)
        self.cam = cam
        self.cmap = get_colormap(cmap)
        self._make_plotter()

    def _load_settings(self, tl: Union[float, None], tr: Union[float, None],
                       asc: Union[float, None], dbg: Union[bool, None]) -> Tuple[float, float, float, bool]:
        r"""
        Returns:
            loads the tiplength, tipradius and arrowscale depending on the inputs and the lattice type
        """
        # Decide on loading settings
        if self.lattice.source == LATT_TYPE_SPIN:
            print(f'loading defaults for type: {LATT_TYPE_SPIN}')
            tiplength = SPINDEFAULT_SETTINGS['tiplength']
            tipradius = SPINDEFAULT_SETTINGS['tipradius']
            arrowscale = SPINDEFAULT_SETTINGS['arrowscale']
            drawbackground = SPINDEFAULT_SETTINGS['drawbackground']
        elif self.lattice.source == LATT_TYPE_EVEC:
            print(f'loading defaults for type: {LATT_TYPE_SPIN}')
            tiplength = EVECDEFAULT_SETTINGS['tiplength']
            tipradius = EVECDEFAULT_SETTINGS['tipradius']
            arrowscale = EVECDEFAULT_SETTINGS['arrowscale']
            drawbackground = EVECDEFAULT_SETTINGS['drawbackground']
        else:
            raise ValueError('Not a valid lattice source!')
        if tl is not None:
            print('Overwriting tiplength setting with user input')
            tiplength = tl
        if tr is not None:
            print('Overwriting tiplradius setting with user input')
            tiplength = tr
        if asc is not None:
            print('Overwriting arrowscale setting with user input')
            tiplength = asc
        if dbg is not None:
            print('Overwriting drawbackground setting with user input')
            drawbackground = dbg
        return tiplength, tipradius, arrowscale, drawbackground

    def _make_plotter(self, offscreen: bool = False):
        r"""
        Creates the plotter. The plotter will be recreated when saving the image
        """
        self.plotter = pv.Plotter(off_screen=offscreen, lighting='three lights')
        self._configureplotter()
        self.plotter.camera_position = self.cam
        plotpoints, plotspins, plotsz = self._make_plot_points()
        self.PolyData = pv.PolyData(plotpoints)
        self.PolyData.vectors = plotspins
        self.PolyData['oop'] = plotsz
        if self.lattice.source == LATT_TYPE_SPIN:
            self.Glyphs = self.PolyData.glyph(orient=True, scale=True, geom=self._geom)
        elif self.lattice.source == LATT_TYPE_EVEC:
            self.Glyphs = self.PolyData.glyph(orient=True, scale=True, geom=self._geom)
        self.plotter.add_mesh(self.Glyphs, show_scalar_bar=False, cmap=self.cmap)
        if self.stat_moms:
            self._draw_statistical_moments()
        if self.total_mag:
            self._draw_total_magnetization()
        if self.drawbackground:
            self._draw_background()

    def _draw_total_magnetization(self) -> None:
        r"""
        Returns:
            the total magnetization (the sum of all spins) in the center of the lattice
        """
        length_tot_mag = np.linalg.norm(self.lattice.total_magnetization)

        if self.lattice.source == 'evec':
            if length_tot_mag < 50:
                print('WARNING: the norm of the total magnetization is below 50. The visualization of it might not be '
                      'visible!')
            arrow = pv.Arrow(start=self.lattice.midpoint, direction=self.lattice.total_magnetization, tip_length=0.25,
                             tip_radius=0.1, tip_resolution=20,
                             shaft_radius=0.05, shaft_resolution=20, scale=length_tot_mag / 10)
        else:
            if length_tot_mag < 500:
                print('WARNING: the norm of the total magnetization is below 500. The visualization of it might not be '
                      'visible!')
            arrow = pv.Arrow(start=self.lattice.midpoint, direction=self.lattice.total_magnetization, tip_length=0.25,
                         tip_radius=0.1, tip_resolution=20,
                         shaft_radius=0.05, shaft_resolution=20, scale=length_tot_mag/100)
        self.plotter.add_mesh(arrow, color='k')

    def _draw_statistical_moments(self) -> None:
        r"""
        Presents the statistical moments of the vector field.
        """
        for stat_mom_nr in range(self.stat_mom_nr):
            if stat_mom_nr == 0:
                mx_center = self.lattice.xmagcenter
                my_center = self.lattice.ymagcenter
                mz_center = self.lattice.zmagcenter
                origin = np.array([0.0, 0.0, 0.0])
                pd_mx = pv.PolyData(mx_center)
                pd_or = pv.PolyData(origin)
                pd_my = pv.PolyData(my_center)
                pd_mz = pv.PolyData(mz_center)
                self.plotter.add_mesh(pd_mx, color='red', point_size=30)
                self.plotter.add_mesh(pd_my, color='green', point_size=30)
                self.plotter.add_mesh(pd_mz, color='blue', point_size=30)
                self.plotter.add_mesh(pd_or, color='k', point_size=30)

    def _draw_background(self) -> None:
        r"""
        Draws the background of the lattice
        """
        for layer in range(self.lattice.nlayer):
            magstruct = self.lattice.getlayer_by_idx(layer)
            points = magstruct[:, :3]
            points_poly = pv.PolyData(points)
            surface = points_poly.delaunay_2d()
            self.plotter.add_mesh(surface, show_edges=True, opacity=0.5)

    def _make_plot_points(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        r"""
        We always want to norm the colormap in the interval -1, 1 even we have a lattice which spins have only SZ comp.
        in the interval e.g. (1,0.5). There is now easy way to do this with pyvista since there is no interface for nor-
        malizing. Therefore, we add an invisible point in the center of the lattice here.

        Returns:
            the points, the spins and the sz components
        """
        plotpoints = np.append(self.lattice.points, np.array([self.lattice.midpoint, self.lattice.midpoint]), axis=0)
        plotspins = np.append(self.lattice.spins, np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]), axis=0)
        if self.lattice.source == LATT_TYPE_SPIN:
            plotsz = np.append(self.lattice.SZ, np.array([1.0, -1.0]))
        elif self.lattice.source == LATT_TYPE_EVEC:
            ez = np.array([0.0, 0.0, 1.0])
            plotsz = [np.dot(spin / np.linalg.norm(spin), ez) for spin in self.lattice.spins]
            plotsz = np.append(plotsz, np.array([1.0, -1.0]))
        else:
            raise ValueError('Lattice type not supported.')
        return plotpoints, plotspins, plotsz

    def _configureplotter(self) -> None:
        r"""
        Configures the plotter object
        """
        pv.set_plot_theme("ParaView")
        pv.rcParams['transparent_background'] = True
        self.plotter.set_background('white')

        def cam() -> None:
            print('Camera postion: ', self.plotter.camera_position)

        self.plotter.add_key_event('c', cam)

    def show(self) -> None:
        r"""
        Shows the plotter
        """
        print('Look what you have done.......')
        print('to get current cam-position press key c')
        self.plotter.show()

    def __call__(self, outpath: Path = Path.cwd() / 'spin.png') -> None:
        r"""
        Saves the image to a file

        Args:
            outpath(Path): output path for the png image created.
        """
        self._make_plotter(offscreen=True)
        self.plotter.window_size = [4000, 4000]
        self.plotter.screenshot(str(outpath.stem))
