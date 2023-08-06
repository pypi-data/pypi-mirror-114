#  Copyright (c) 2021 XPL Technologies AB - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary software
#  Written by Ivan Korol, 2021

from xplai.api import modality_api_client

from xplai.cli import utils


def list_supported_modalities():
    modalities = modality_api_client.get_supported_modalities()

    for modality in modalities:
        modality['supported_model_sizes'] = str(modality['supported_model_sizes'])

    modalities_summary_text = '\nSupported modalities:\n'
    modalities_summary_text += utils.print_table(modalities, ['modality_id', 'supported_model_sizes'])

    return modalities_summary_text


def __get_modality_summary_text(modality):
    summary = f'~~~~~~~~~~~~~~~~~~~~[{modality["modality_id"]}]~~~~~~~~~~~~~~~~~~~~~~~\n' \
              f'Supported model sizes: {modality["supported_model_sizes"]}\n'
    return summary
