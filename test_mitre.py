# from modules.mitre_mapper import MitreMapper

# mapper = MitreMapper()

# print(mapper.map_event("Download File"))

from modules.mitre_mapper import MitreMapper


mapper = MitreMapper()

result = mapper.map_event("usb")

print(result)