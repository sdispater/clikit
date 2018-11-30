from typing import List

from pylev import levenshtein

from clikit.api.command import CommandCollection


def find_similar_command_names(
    name, commands
):  # type: (str, CommandCollection) -> List[str]
    """
    Finds names similar to a given command name.
    """
    threshold = 1e3
    distance_by_name = {}

    # Include aliases in the search
    actual_names = commands.get_names(True)

    for actual_name in actual_names:
        # Get Levenshtein distance between the input and each command name
        distance = levenshtein(name, actual_name)

        is_similar = distance <= len(name) / 3
        is_sub_string = actual_name.find(name) != -1

        if is_similar or is_sub_string:
            distance_by_name[actual_name] = distance

        # Only keep results with a distance below the threshold
        distance_by_name = {
            k: v for k, v in distance_by_name.items() if v < 2 * threshold
        }

        # Display results with shortest distance first
        suggested_names = []
        for k, v in sorted(distance_by_name.items(), key=lambda _, v: v):
            if k not in suggested_names:
                suggested_names.append(k)

        return suggested_names
