import os
from datetime import datetime, timedelta
import re
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def dtv_parser(filepath: str, order='asc', as_datetime=True) -> dict:
    """Parse dtv type file

    :param filepath: Dtv filepath
    :param order: Timestamp order (asc or desc)
    :param as_datetime: return timestamps as datetime obj
    :return: {id: <id>, unit: <unit>, values: [(<timestamp>, <value>),..}
    """

    if order and not as_datetime:
        raise ValueError('Invalid arguments, `order` must be used together with `as_datetime`')

    with open(filepath, 'rb') as f:
        lines = []
        for line in f:
            decoded_line = line.decode(errors='ignore', encoding='windows-1252')
            lines.append(decoded_line)

    unit = (''.join(x.lstrip().rstrip() for x in lines[:6])).lstrip('Â')
    name, _ = os.path.splitext(os.path.basename(filepath))
    device = name.split('_')[0]
    channel = "_".join(name.split('_')[1:])
    device_id = f'{device}.{channel}'

    values = []

    for line in lines:
        try:
            match = re.match('(.*),(.*)', line.strip())
            if match:
                timestamp = match.group(1)
                if len(match.group(1).split('.')) == 1:
                    if as_datetime:
                        timestamp = datetime.strptime(match.group(1), '%d/%m/%Y %H:%M:%S')
                else:
                    if as_datetime:
                        timestamp = datetime.strptime(match.group(1), '%d/%m/%Y %H:%M:%S.%f')
                value = eval(match.group(2))
            else:
                continue
        except Exception as msg:
            logger.error('Parsing line:{}, e:'.format(line, msg))
            continue

        values.append((timestamp, value))

    if order and as_datetime:
        if order == 'asc':
            values = sorted(values, key=lambda x: x[0])
        if order == 'desc':
            values = sorted(values, key=lambda x: x[0], reverse=True)

    return {'id': device_id, 'unit': unit, 'values': values}


def dtv_write(filepath: str, values: list = None, unit: str = None) -> str:
    """ Write dtv file

    :param filepath: Dtv filepath
    :param values: Values to write
    :param unit: Unit
    :return: Dtv filepath
    """

    header = ['\n', '\n', unit, '\n', '\n', '\n', '\n', '\n', '\n', '\n']
    body = []
    for i in values:
        ts = i[0]
        val = i[1]
        ts_str = ts.strftime("%d/%m/%Y %H:%M:%S")
        body.append(f'{ts_str},{val}\n')
    with open(filepath, 'w') as f:
        f.writelines(header + body)
    return filepath


def dtv_to_pandas(filepath) -> pd.DataFrame:
    """ Convert dtv type file to pandas
    :param filepath:
    :return: Pandas dataframe
    """
    values = dtv_parser(filepath)
    if values['values']:
        d = {'timestamp': [i[0] for i in values['values']], 'values': [i[1] for i in values['values']]}
        print(d)
        df = pd.DataFrame(data=d).set_index(['timestamp'])
    else:
        df = pd.DataFrame(data={'timestamp': [], 'values': []})
    return df


def compensate_files(filepath: str, filepath_comp: str = None, filepath_out: str = None,
                     offset: float = None, operator='-', max_tolerance: float = None) -> str:
    """
    Compensate two files.
    Take file and find closest measurement in file_comp and perform math: file <operator> file_comp

    :param filepath: Filepath in
    :param filepath_comp: Filepath for compensation
    :param filepath_out: Filepath out
    :param offset: Data offset
    :param operator: Math operator between input file and compensation file (-,+,*)
    :param max_tolerance: Max timestamp tolerance [minutes]
    :return: result filepath
    """

    if not filepath:
        raise ValueError('Invalid value for `filepath`, must not be `None`')

    if not filepath_out:
        filename_out = f'{os.path.basename(filepath)}_kompenzirano.dtv'
        filepath_out = os.path.join(os.path.dirname(filepath), filename_out)

    data_in = dtv_parser(filepath=filepath, as_datetime=True)

    df_comp = None
    if filepath_comp:
        df_comp = dtv_to_pandas(filepath=filepath_comp)

    values_out = []
    for i in data_in['values']:
        ts = i[0]
        val = i[1]
        val_out = val
        if filepath_comp:
            try:
                if max_tolerance is not None:
                    comp_index = df_comp.index.get_loc(ts, method='nearest', tolerance=timedelta(minutes=max_tolerance))
                else:
                    comp_index = df_comp.index.get_loc(ts, method='nearest')
                val_comp = df_comp.values[comp_index][0]
                val_out = eval(f'{val} {operator} {val_comp}')
            except KeyError:
                # No match was found within range
                logger.warning(f'No match was found in file `{filepath_comp}` within tolerance {max_tolerance}s')
                continue

        if offset:
            val_out += offset

        values_out.append((ts, val_out))

    return dtv_write(filepath=filepath_out, unit=data_in['unit'], values=values_out)


