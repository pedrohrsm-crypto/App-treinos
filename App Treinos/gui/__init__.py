"""
GUI Package - Interface Gráfica do App Treinos
==============================================
"""

from .theme import theme, AccessibleTheme
from .main_gui import AppTreinosGUI
from .progress_dashboard import ProgressDashboard
from .fitness_screen import FitnessScreen

__all__ = ['theme', 'AccessibleTheme', 'AppTreinosGUI', 'ProgressDashboard', 'FitnessScreen']
