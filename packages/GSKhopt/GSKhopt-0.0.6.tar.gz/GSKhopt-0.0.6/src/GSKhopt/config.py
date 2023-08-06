import json
def parse_config(filepath):
    with open(filepath) as f:
        data = json.load(f)
        parameters_names = []
        upper_limit = []
        lower_limit = []
        ignore_tracking = []
        ranges = dict()
        for parameter_name in data.keys():
            #build a list of upper_limit and lower_limits for GSKpy
            parameter = data[parameter_name]
            if "range" in parameter:
                if "depends" in parameter:
                    dependable_max_size = data[parameter["depends"]]["range"][1]
                    for i in range(dependable_max_size):
                        lower_limit.append(parameter["range"][0])
                        upper_limit.append(parameter["range"][1])
                        parameters_names.append(str(i)+"_"+parameter_name)
                else:
                    lower_limit.append(parameter["range"][0])
                    upper_limit.append(parameter["range"][1])
                    parameters_names.append(parameter_name)


            elif "categorical" in parameter:
                if "depends" in parameter:
                    dependable_max_size = data[parameter["depends"]]["categorical"][-1]
                    for i in range(dependable_max_size):
                        lower_limit.append(parameter["categorical"][0])
                        upper_limit.append(parameter["categorical"][-1])
                        parameters_names.append(str(i)+"_"+parameter_name)
                        ranges[str(i)+"_"+parameter_name] = parameter["categorical"]
                else:
                    lower_limit.append(parameter["categorical"][0])
                    upper_limit.append(parameter["categorical"][-1])
                    parameters_names.append(parameter_name)
                    ranges[parameter_name] = parameter["categorical"]

            elif parameter_name == "ignore_tracking":
                #ignore_tracking
                ignore_tracking = parameter
            else:
                #something is wrong with your json file
                raise("something is wrong with your config file")
    return parameters_names,lower_limit,upper_limit,ranges
