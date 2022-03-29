import json
import lizard


def find_corresponding_function(name, analyzed_file_after_fix, file_after_fix):
    found = False
    function_start_line = 0
    function_end_line = 0
    for function in analyzed_file_after_fix.function_list:
        function_dict = function.__dict__
        if function_dict["long_name"].replace(" ", "") == name.replace(" ", ""):
            found = True
            function_start_line = int(function_dict["start_line"])
            function_end_line = int(function_dict["end_line"])
            break
    
    file_after_fix_lines = file_after_fix.splitlines()
    function_after_fix_lines = file_after_fix_lines[(function_start_line-1):(function_end_line+1)]
    functon_after_fix = "\n".join(function_after_fix_lines)
    
    return functon_after_fix

if __name__ == "__main__":
    path = "mined_bug/0/sstubs.json"

    f = open(path)
 
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    
    new_json = []
    for sstub in data:
        print("-----------------------")
        output_dict = {}

        file_before_fix = sstub["fileBeforeFix"]
        file_after_fix = sstub["fileAfterFix"]
        file_before_fix_lines = file_before_fix.splitlines()
        # print(file_before_fix)
        bug_line_num = int(sstub["bugLineNum"])
        analyzed_file_before_fix = lizard.analyze_file.analyze_source_code("AllTests.java", file_before_fix)
        analyzed_file_after_fix = lizard.analyze_file.analyze_source_code("AllTests.java", file_after_fix)
        # print(i.__dict__)
        print(sstub["sourceBeforeFix"])
        print(sstub["sourceAfterFix"])
        output_dict["bugType"] = sstub["bugType"]
        output_dict["fixCommitSHA1"] = sstub["fixCommitSHA1"]
        output_dict["projectName"] = sstub["projectName"]
        output_dict["sourceBeforeFix"] = sstub["sourceBeforeFix"]
        output_dict["sourceAfterFix"] = sstub["sourceAfterFix"]

        can_find_function = False
        for function in analyzed_file_before_fix.function_list:
            function_dict = function.__dict__
            function_start_line = int(function_dict["start_line"])
            function_end_line = int(function_dict["end_line"])

            # This means that we have identified the buggy function.
            if function_start_line <= bug_line_num <= function_end_line:
                can_find_function = True
                function_before_fix_lines = file_before_fix_lines[(function_start_line-1):(function_end_line+1)]
                function_before_fix_content = "\n".join(function_before_fix_lines)
                bug_line_num_in_file = bug_line_num - function_start_line

                function_after_fix_content = find_corresponding_function(function_dict["long_name"], analyzed_file_after_fix, file_after_fix)
                
                print(function_before_fix_content)
                print("$$$$$$$")
                print(function_after_fix_content)

                
                line_before_fix = file_before_fix.splitlines()[bug_line_num-1]
                line_after_fix = ""
                for line in function_after_fix_content.splitlines():
                    line_temp = line.replace(" ", "")
                    if sstub["sourceAfterFix"].replace(" ", "") in line_temp:
                        line_after_fix = line
                # line_after_fix = line_before_fix.replace(sstub["sourceBeforeFix"], sstub["sourceAfterFix"])
                
                print(line_before_fix)
                print(line_after_fix)
                output_dict["bugLineNumInFile"] = bug_line_num_in_file
                output_dict["functionBeforeFix"] = function_before_fix_content.lstrip()
                output_dict["functionAfterFix"] = function_after_fix_content.lstrip()
                output_dict["lineBeforeFix"] = line_before_fix.lstrip()
                output_dict["lineAfterFix"] = line_after_fix.lstrip()
        
        if can_find_function == True:
            new_json.append(output_dict)

    with open('processed_data/function_sstubs_v1_0.json', 'w', encoding='utf-8') as f1:
        json.dump(new_json, f1, ensure_ascii=False, indent=4)