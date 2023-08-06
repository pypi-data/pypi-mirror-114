"""Deetly."""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from deetly import datapackage
from deetly import validator
#from deetly import echarts

metadata = datapackage.Datapackage
package = datapackage.Datapackage
story = datapackage.Datapackage
#Map = echarts.Map
#JsCode = echarts.JsCode
#pyecharts = echarts.pyecharts
#echarts = echarts.echarts
