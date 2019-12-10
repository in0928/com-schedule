from difflib import SequenceMatcher


def merge_rows(cursor):
    new_list = []
    for item in cursor:
        new_list.append(item) # a list of dics

    for i in range(len(new_list)):
        e1 = new_list[i]  # use the first entry as standard

        indice_of_duplicates = []

        count = i + 0

        for entry in new_list[i + 1:]:  # from forward
            if e1["content"] == "" or e1["content"] == "Invisible":
                count += 1
                continue
            elif similar_enough(e1["content"], entry["content"]) and \
                    similar_enough(e1["time"], entry["time"]) and \
                    similar_enough(e1["SP"], entry["SP"]) and \
                    similar_enough(e1["venue"], entry["venue"]):
                indice_of_duplicates.append(count + 1)
                count += 1
            else:
                count += 1
                continue

        names = [e1["union_name"]]
        for index in indice_of_duplicates:
            name = new_list[index]["union_name"]
            names.append(name)
            new_list[index]["content"] = "Invisible"  # cannot set to "", will cause problem

        new_name = ", ".join(names)  # should be like "A, B, C"
        e1["union_name"] = new_name

    return new_list


def similar_enough(s1, s2):
    s = SequenceMatcher(None, s1.lower().strip(), s2.lower().strip()).ratio()
    if s > 0.85:
        return True
    return False



