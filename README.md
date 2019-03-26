Sample Python 3 code to generate a json output simular to the format generated by:
  http://api.brain-map.org/api/v2/structure_graph_download/1.json

# Setup Python 3 environment within RHEL 6.
scl enable rh-python36 bash
# Make sure we are running Python 3
python -V

# Run program
./ara2json.py ara2.csv arat2.csv > result.json


