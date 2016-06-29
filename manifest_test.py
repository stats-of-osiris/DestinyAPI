import destiny
import json

john = destiny.Player('psn', 'JohnOfMars')

# print(
#     json.dumps(
#         titan.data,
#         indent=4
#     )
# )

# print(
#     titan.player_name
# )
#
# print(
#     john.guardians
# )

guardian_id = john.guardians.loc[
    (john.guardians['class'] == 'Titan')].index.values[0]

print(
    guardian_id
)

titan = destiny.Guardian('psn', 'JohnOfMars', guardian_id)

print(
    titan.player_name
)

