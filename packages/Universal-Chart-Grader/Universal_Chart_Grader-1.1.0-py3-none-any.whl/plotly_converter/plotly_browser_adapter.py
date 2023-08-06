"""
Adapter of browser using selenium
"""

import selenium.webdriver
import selenium.webdriver.chrome.options

browser = None


def start_browser(headless=True):
    """
    start an browser instance and return the python handle

    Args:
        headless: if True, start browser in background

    Returns: browser object

    """

    if browser is not None:
        return browser

    chrome_options = selenium.webdriver.chrome.options.Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--use-gl")

    driver = selenium.webdriver.Chrome()

    return driver


class BrowserFigure:
    """ Plotly figure in the browser """

    def __init__(self, browser):
        self.browser = browser

    def evalJS(self, js):
        return self.browser.execute_script(
                'gd = document.querySelector(".plotly-graph-div")' + '\n' + js)

    def scene_attr(self, scene_key, field):
        return self.evalJS(f"gd._fullLayout['{scene_key}']['{field}']")

    def polar_attr(self, polar_key, field):
        return self.evalJS(f"gd._fullLayout['{polar_key}']['{field}']")

    def cart2d_axis_attr(self, axis_key, field):
        return self.evalJS(f"gd._fullLayout['{axis_key}']['{field}']")

    def cart3d_xaxis_attr(self, scene_key, field):
        return self.evalJS(f"gd._fullLayout['{scene_key}'].xaxis['{field}']")

    def cart3d_yaxis_attr(self, scene_key, field):
        return self.evalJS(f"gd._fullLayout['{scene_key}'].yaxis['{field}']")

    def cart3d_zaxis_attr(self, scene_key, field):
        return self.evalJS(f"gd._fullLayout['{scene_key}'].zaxis['{field}']")

    def angularaxis_attr(self, polar_key, field):
        return self.evalJS(f"gd._fullLayout['{polar_key}'].angularaxis['{field}']")

    def radialaxis_attr(self, polar_key, field):
        return self.evalJS(f"gd._fullLayout['{polar_key}'].radialaxis['{field}']")

    def cart2d_tick_vals(self, axis_key):
        return self.evalJS(f"gd._fullLayout['{axis_key}'].tickvals")

    def cart2d_tick_vals_tickvals(self, axis_key):
        return self.evalJS(
                "gd._fullLayout['$axis_key']._vals.map(function(x){return x.x})".replace('$axis_key', axis_key))

    def cart2d_tick_labels(self, axis_key):
        return self.evalJS(
                "gd._fullLayout['$axis_key']._vals.map(function(x){return x.text})".replace('$axis_key', axis_key))

    def tick_labels(self, subplot_key, tick_key):
        js = f"""
        ticks = document.querySelectorAll(".{subplot_key} .{tick_key}");
        ticks = Array.from(ticks); """
        js += "ticks.map(function(x){return x.__data__.text})"
        return self.evalJS(js)

    def tick_vals(self, subplot_key, tick_key):
        js = f"""
        ticks = document.querySelectorAll(".{subplot_key} .{tick_key}");
        ticks = Array.from(ticks); """
        js += "ticks.map(function(x){return x.__data__.x})"
        return self.evalJS(js)

    def figure_width(self):
        return self.evalJS('gd._fullLayout._size.w')

    def figure_height(self):
        return self.evalJS('gd._fullLayout._size.h')

    def figure_title(self):
        return self.evalJS('return gd._fullLayout.title')
