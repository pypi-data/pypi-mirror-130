import pandas as pd
import numpy as np
import scipy.stats as stats

import warnings

import matplotlib.pyplot as plt

import bluebelt.core.helpers
import bluebelt.core.decorators

import bluebelt.data.resolution

import bluebelt.styles

@bluebelt.core.decorators.class_methods


class Effort():
    """
    Calculate the planning effort
    """
    def __init__(self, series, how='group', rule='iso_jaar-iso_week', **kwargs):
        
        self.series = series
        self.how = how
        self.rule = rule

        # get qdq variable columns
        self.quantity = kwargs.pop('quantity', None) or kwargs.pop('q', None)
        self.distribution = kwargs.pop('distribution', None) or kwargs.pop('dist', None) or kwargs.pop('d', None)
        self.quality = kwargs.pop('quality', None) or kwargs.pop('skills', None) or kwargs.pop('s', None)
        
        print(self.quantity)
        print(self.distribution)
        print(self.quality)
        
        self.calculate()

    def calculate(self):

        if self.how == 'group':
            self.quantity = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, rule=self.rule).inter_scale().result
            self.distribution = bluebelt.data.resolution.GroupByDatetimeIndex(self.series, rule=self.rule).intra_scale().result
        

    def __repr__(self):
        return (f'{self.__class__.__name__}(n={self.series.size:1.0f}, quantity={self.quantity.mean():1.4f}, distribution={self.distribution.mean():1.4f})')
    
    def plot(self, **kwargs):
        
        return _qdq_plot(self, **kwargs)

def _qdq_plot(_obj, **kwargs):
        
    style = kwargs.pop('style', bluebelt.styles.paper)
    title = kwargs.pop('title', f'{_obj.series.name} Effort QDQ plot')
    
    path = kwargs.pop('path', None)
    xlim = kwargs.pop('xlim', (None, None))
    ylim = kwargs.pop('ylim', (0, None))
    
    # prepare figure
    fig, axes = plt.subplots(nrows=1, ncols=1, **kwargs)

    axes.fill_between(_obj.quantity.index, 0, _obj.quantity.values, **style.planning.fill_between_inter, label='quantity')
    axes.plot(_obj.inter, **style.planning.plot_quantity, **kwargs)

    axes.fill_between(_obj.distribution.index, 0, _obj.distribution.values, **style.planning.fill_between_intra, label='distribution')
    axes.plot(_obj.intra, **style.planning.plot_distribution, **kwargs)

    # format things
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)
    
    # title
    axes.set_title(title, **style.graphs.line.title)

    # legend
    axes.legend(loc='upper left')

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig