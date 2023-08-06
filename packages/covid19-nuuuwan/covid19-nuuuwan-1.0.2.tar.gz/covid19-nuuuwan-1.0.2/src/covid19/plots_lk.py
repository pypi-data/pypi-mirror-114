"""Example 10."""

import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np
from utils import timex

from covid19 import lk_data

BASE_IMAGE_FILE = 'src/covid19/assets/lk_map.png'
FONT_FILE = 'src/covid19/assets/Arial.ttf'
DAYS_PLOT = 90
MW = 7
POPULATION = 21_800_000


def _plot_with_time_window(
    field_key,
    main_color,
    sub_color,
    label,
    is_background_image=False,
):
    timeseries = lk_data.get_timeseries()
    date_id = timex.format_time(timeseries[-1]['unixtime'], '%Y%m%d')
    date = timex.format_time(timeseries[-1]['unixtime'], '%Y-%m-%d')
    x = list(
        map(
            lambda d: datetime.datetime.fromtimestamp(d['unixtime']),
            timeseries[-DAYS_PLOT:],
        )
    )
    y = list(map(lambda d: d[field_key], timeseries[-DAYS_PLOT:]))
    plt.bar(x, y, color=sub_color)

    x2 = list(
        map(
            lambda d: datetime.datetime.fromtimestamp(
                d['unixtime'] + MW * 86400
            ),
            timeseries[(-DAYS_PLOT - MW):],
        )
    )
    y2 = list(map(lambda d: d[field_key], timeseries[(-DAYS_PLOT - MW):]))
    y2 = np.convolve(y2, np.ones(MW) / MW, 'valid')

    plt.plot(x2[: -(MW - 1)], y2, color=main_color)
    plt.title('%s with a %d-Day Moving Avg. (as of %s)' % (label, MW, date))
    plt.suptitle(
        'Data: https://github.com/CSSEGISandData/COVID-19; '
        + 'https://www.hpb.health.gov.lk/api/get-current-statistical; '
        + 'https://github.com/owid/covid-19-data',
        fontsize=8,
    )

    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        tkr.FuncFormatter(lambda x, p: format(int(x), ','))
    )

    fig = plt.gcf()
    fig.autofmt_xdate()
    fig_width = 12
    aspect_ratio = 3 if is_background_image else 16 / 9
    fig_height = round(fig_width / aspect_ratio, 1)
    fig.set_size_inches(fig_width, fig_height)

    background_label = 'background' if is_background_image else 'feed'
    image_file = '/tmp/covid19.plot.%s.%s.%s.window.png' % (
        date_id,
        field_key,
        background_label,
    )
    fig.savefig(image_file, dpi=100)
    plt.close()
    return image_file


def _plot_simple(field_key, main_color, label):
    timeseries = lk_data.get_timeseries()
    date_id = timex.get_date_id(timeseries[-1]['unixtime'])
    date = timex.format_time(timeseries[-1]['unixtime'], '%Y-%m-%d')

    x = list(
        map(
            lambda d: datetime.datetime.fromtimestamp(d['unixtime']),
            timeseries[-DAYS_PLOT:],
        )
    )
    y = list(map(lambda d: d[field_key], timeseries[-DAYS_PLOT:]))
    plt.plot(x, y, color=main_color)

    plt.title('%s (as of %s)' % (label, date))
    plt.suptitle(
        'Data: https://github.com/CSSEGISandData/COVID-19; '
        + 'https://www.hpb.health.gov.lk/api/get-current-statistical; '
        + 'https://github.com/owid/covid-19-data',
        fontsize=8,
    )

    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(
        tkr.FuncFormatter(lambda x, p: format(int(x), ','))
    )

    fig = plt.gcf()
    fig.autofmt_xdate()
    fig.set_size_inches(12, 6.75)
    image_file = '/tmp/covid19.plot.%s.%s.simple.png' % (date_id, field_key)
    fig.savefig(image_file, dpi=100)
    plt.close()
    return image_file
