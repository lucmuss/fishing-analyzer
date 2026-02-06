from fishing_analyzer import config
from fishing_analyzer.utils import get_year_range

print("Configured Mongo URI:", config.MONGODB_URI)
print("Supported years:", get_year_range(config.MINIMAL_BEGIN_DATE, config.MAXIMAL_END_DATE))
