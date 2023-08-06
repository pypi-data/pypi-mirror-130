import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt

from bluebelt.core.checks import check_kwargs

import bluebelt.core.decorators

import bluebelt.data.index


import warnings

def resolution_methods(cls):

    def sum(self):
        result = self.grouped.sum()
        result._blue_function = 'sum'
        return result

    def mean(self):
        return self.grouped.mean()

    def var(self):
        return self.grouped.var()

    def std(self):
        return self.grouped.std()

    def min(self):
        return self.grouped.min()

    def max(self):
        return self.grouped.max()
    
    def count(self):
        return self.grouped.count()
    
    def value_range(self):
        return self.grouped.apply(lambda x: x.max() - x.min())

    def inter_scale(self):
        return ( (self.grouped.sum() - self.grouped.sum().shift()) / self.grouped.sum().shift() ).abs().fillna(0)

    def intra_scale(self, **kwargs):

        values = kwargs.get('values', None)

        # _obj = self._obj[values] if isinstance(self._obj, pd.DataFrame) and values is not None else
        
        if isinstance(self._obj, pd.Series):
            index_groups = self.grouped.obj.index.names

            if (self.grouped.obj.index.names.index(self.level) + 1) < len(index_groups):
                group = index_groups[self.grouped.obj.index.names.index(self.level) + 1]
                result = self.grouped.apply(lambda s: s.groupby(group).sum()).unstack(level=-1)
                result = pd.Series((result - result.shift().multiply((result.sum(axis=1) / result.sum(axis=1).shift()), axis=0)).abs().sum(axis=1) / (result.sum(axis=1) * 2), name=self._obj.name)
            else:
                result = pd.Series(index=self.grouped.sum().index, data=[0]*self.grouped.sum().size, name=self._obj.name)

            return result
        else:
            raise ValueError("intra_scale can not be called form a pandas.DataFrame Groupby object")
    

    def subsize_count(self, count=3, size=1):
        """
        Count the number of times a list of <count> items with size <size> fit in the groupby object (which is a pandas Series)
        e.g.
        groupby object: pd.Series([10, 8, 3, 3, 5])
        count = 3
        size = 1

        returns 9

        step 0: (3, 3, 5, 8, 10)
        step 1: (3, 3, 4, 7, 9)
        step 2: (3, 3, 3, 6, 8)
        step 3: (2, 3, 3, 5, 7)
        step 4: (2, 2, 3, 4, 6)
        step 5: (2, 2, 2, 3, 5)
        step 6: (1, 2, 2, 2, 4)
        step 7: (1, 1, 1, 2, 3)
        step 8: (0, 1, 1, 1, 2)
        step 9: (0, 0, 0, 1, 1)

        """
        if isinstance(count, (float, int)):
            count = [int(count)]
        
        result = {}
        for c in count:
            result[c] = self.grouped.apply(lambda x: _subsize_count(series=x, count=c, size=size)).values
        self.grouped = pd.DataFrame(result, index=self.grouped.groups.keys()) #self.grouped.apply(lambda x: _subsize_count(series=x, count=count, size=size))
        self.func = f'count subsize (count={count}, size={size})'
        
        if len(count) == 2:
            d = {}
            #arr = self.grouped.values.T
            for val in range(int(self.grouped.values.min()), int(self.grouped.values.max())):
                
                if self.grouped.iloc[:,0].mean() > self.grouped.iloc[:,1].mean():
                #if arr[0].mean() > arr[1].mean():
                    d[val] = self.grouped.shape[0] - self.grouped[(self.grouped.iloc[:,0]>val) & (self.grouped.iloc[:,1]<val)].shape[0]
                    #d[val] = arr[0][arr[0]<val].size + arr[1][arr[1]>val].size
                else:
                    d[val] = self.grouped.shape[0] - self.grouped[(self.grouped.iloc[:,0]<val) & (self.grouped.iloc[:,1]>val)].shape[0]
                    #d[val] = arr[0][arr[0]>val].size + arr[1][arr[1]>val].size

            out_of_bounds = np.min(list(d.values()))
            keys = list({key:value for (key,value) in d.items() if value == out_of_bounds}.keys())
            
            self.optimum = (np.min(keys), np.max(keys))
            self.out_of_bounds = out_of_bounds
        else:
            self.optimum = None
            self.out_of_bounds = None

        return self

    def subseries_count(self, subseries=None, **kwargs):
        """
        Count the number of times a subseries of wil fit in the groupby object (which is a pandas Series)
        
        Under construction!! Not valid on extreme value differences...

        e.g.
        groupby object: pd.Series([10, 8, 3, 3, 5])
        subseries: pd.Series([1, 2, 3])

        returns 4

        step 0: (3, 3, 5, 8, 10)
        step 1: (3, 3, 4, 6, 7)
        step 2: (3, 3, 3, 4, 4)
        step 3: (2, 3, 3, 2, 1)
        step 4: (1, 1, 0, 2, 1)

        """
        self.grouped = self.grouped.apply(lambda x: _subseries_count(series=x, subseries=subseries, **kwargs))
        self.func = f'count subseries (subseries={list(subseries)})'
        return self

    def graph(self, **kwargs):

        if self.func == '':
            series = self.grouped.sum()
            func = 'sum'
        else:
            series = self.grouped
            func = self.func

        style = kwargs.pop('style', bluebelt.styles.paper)
        path = kwargs.pop('path', None)

        xlim = kwargs.pop('xlim', (None, None))
        ylim = kwargs.pop('ylim', (None, None))

        fig, ax = plt.subplots(**kwargs)

        # observations
        ax.plot(series, **style.resolution.plot)

        xlims = ax.get_xlim()
        
        # mean
        if hasattr(self, 'optimum'):
            if self.optimum is not None:
                ax.fill_between(xlims, self.optimum[0], self.optimum[1], **style.resolution.optimum_fill_between)
                ax_text = f'bounds: {self.optimum[0]:1.0f} - {self.optimum[1]:1.0f}\nout of bounds: {self.out_of_bounds}'
                ax.text(0.02, 0.98, ax_text, transform=ax.transAxes, **style.resolution.bounds_text)
            else:
                ax.axhline(series.values.mean(), **style.resolution.axhline)
                ax.text(series.index.values.min(), series.values.mean(), f'{series.values.mean():1.2f}', **style.resolution.text)

        # labels
        ax.set_title(f'{self._obj.name} grouped', **style.resolution.title)
        ax.set_xlabel(self.level)
        ax.set_ylabel(func)

        #reset xlim
        ax.set_xlim(xlims)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    

        if path:
            plt.savefig(path)
            plt.close()
        else:
            plt.close()
            return fig

    setattr(cls, 'sum', sum)
    setattr(cls, 'mean', mean)
    setattr(cls, 'var', var)
    setattr(cls, 'std', std)
    setattr(cls, 'min', min)
    setattr(cls, 'max', max)
    setattr(cls, 'count', count)
    setattr(cls, 'value_range', value_range)
    setattr(cls, 'intra_scale', intra_scale)
    setattr(cls, 'inter_scale', inter_scale)
    setattr(cls, 'subsize_count', subsize_count)
    setattr(cls, 'subseries_count', subseries_count)
    
    return cls

@bluebelt.core.decorators.class_methods
@resolution_methods
class GroupByDatetimeIndex():
    """
    Group a pandas.Series or pandas.DataFrame by DateTime index and apply a specific function.
        arguments
        series: pandas.Series
        how: str
            a string with date-time keywords that can be parsed to group the index
            keywords:
            
            default value "week"

        Apply one of the following functions:
            .sum()
            .mean()
            .min()
            .max()
            .std()
            .value_range()
            .count()
            .subsize_count()

        e.g. series.blue.data.group_index(how="week").sum()
        
    """
    
    def __init__(self, _obj, level="week", iso=True, **kwargs):

        self._obj = _obj
        self.level = level
        self.iso = iso
        self.nrows = self._obj.shape[0]
        self.calculate(**kwargs)

    def calculate(self, **kwargs):

        if self.iso and self.level in ['month']:
            warnings.warn(f'rule={self.level} is not possible when using iso=True; iso will be set to False', Warning)
            self.iso = False
        elif not self.iso and self.level in ['week']:
            warnings.warn(f'rule={self.level} is not possible when using iso=False; iso will be set to True', Warning)
            self.iso = True
        
        if self.iso:
            self._obj = bluebelt.data.index.iso_index(self._obj)
        else:
            self._obj = bluebelt.data.index.dt_index(self._obj)

        self.grouped = self._obj.groupby(self._obj.index.names[:self._obj.index.names.index(self.level) + 1])

    def __str__(self):
        return ""
    
    def __repr__(self):
        return self.grouped.__repr__()

def _subsize_count(series, count=3, size=1):
    series = pd.Series(series)/size
    result = series.sum()*count
    for i in range(count, 0, -1):
        result = min(result, math.floor(series.nsmallest(len(series) - count + i).sum() / i))
    return result

def _subseries_count(series, subseries=None, **kwargs):
    series = pd.Series(series)
    subseries = pd.Series(subseries)
    result=series.sum()*subseries.sum()
    for i in range(len(subseries), 0, -1):
        result = min(result, math.floor(series.nsmallest(len(series) - len(subseries) + i).sum() / subseries.nsmallest(i).sum()))
    return result


def _get_index_dict(self):

    if self.iso:
        _dict = {
            'year': self._obj.index.isocalendar().year.rename('year'), # year including the century
            'week': self._obj.index.isocalendar().week.rename('week'), # iso-week of the year (1 to 53)
            'day': self._obj.index.isocalendar().day.rename('day'), # day of the week (1 to 7)
        }
    else:
        _dict = {
            'year': self._obj.index.year.rename('year'), # year including the century
            'month': self._obj.index.month.rename('month'), # month (1 to 12)
            'day': self._obj.index.day.rename('day'), # day of the month (1 to 31)
            'hour': self._obj.index.hour.rename('hour'), # hour, using a 24-hour clock (0 to 23)
            'minute': self._obj.index.minute.rename('minute'),
            'second': self._obj.index.second.rename('second'),
        }

    return _dict


def _get_index(self):
    index = []
    
    level = min(len(self._obj.index.names), self._obj.index.names.index(self.level) + 1)

    for group, values in enumerate(self._obj.index.levels[:level]):
        if values.size > 1:
            index.append(self._obj.index.names[group]) 

    return index