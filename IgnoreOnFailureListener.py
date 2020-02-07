import os.path
import tempfile
import os
import shutil

class IgnoreOnFailureListener(object):
    ROBOT_LISTENER_API_VERSION = 2
    global test_script_name
    global output_file
    test_script_name = ""
    global output_dir_path
    def __init__(self, drive ="D" , folder="Rough" ,  filename1='Detailed_test_case_report.html' , filename2 ='Test Summary Report.html',output_dir="" , output_folder=""):
        #retrieve current working directory
        dirpath = os.getcwd()
        global output_dir_path

        if output_dir.strip()!="":
            output_dir_path="//"+str(os.environ['COMPUTERNAME'])+"/"+output_dir.strip()+output_folder.strip()
        else:
            output_dir_path=os.getcwd()
        print "output_dir_path {}".format(output_dir_path)
        #Copy the two files from the D:/Rough to the current working directory
        list_files = ['Detailed_test_case_report.html', 'Test Summary Report.html']
        #shutil.copyfile(str(dirpath + "\\" + filename1).strip(), str(drive + ":\\" + folder + "\\" + filename1).strip())
        #shutil.copyfile(str(dirpath + "\\" + filename2), str(drive + ":\\" + folder + "\\" + filename2).strip())
        #define variables for the two report files
        global output_file
        output_file = str(drive + ":/" + folder + "/" + filename1).strip()
		#print str(output_file)
        self.summary_output_file = str(drive + ":/" + folder + "/" + filename2).strip()
        #Initialize all the count variables
        self.total_test_cases_executed = 0
        self.total_test_suites_executed = 0
        self.total_test_cases_passed = 0
        self.total_test_cases_failed = 0
        #Initialize test suite name, test case name and keyword variable
        self.test_suite_name = ""
        self.test_case_name=""
        self.keyword = ""
        #Clear the old records
        with open(output_file , 'r') as f:
            str1 = f.read()
        # str2 = str1[:str1.find("<!--Copy till here-->") + len("<!--Copy till here-->")]
        str2 = str1[:str1.find("<!--Execution Status s-->") + len("<!--Execution Status s-->")] + "Execution in progress or Terminated" + str1[str1.find("<!--Execution Status e-->"):str1.find("<!--Copy till here-->") + len("<!--Copy till here-->")]
        self.outfile = open(output_file, 'w')
        self.outfile.write(str2)
        self.outfile.close
        with open(self.summary_output_file , 'r') as f:
            str1 = f.read()
        str2 = str1[:str1.find("<!--Execution Status s-->") + len("<!--Execution Status s-->")] + "Execution in progress or Terminated" + str1[str1.find("<!--Execution Status e-->"):str1.find("<!--Copy till here-->") + len("<!--Copy till here-->")]
        self.outfile2 = open(self.summary_output_file, 'w')
        self.outfile2.write(str2)
        self.outfile2.close
        self.update_file("<!--Execution Status", "Execution is In progress.. or Terminated")
        self.update_stat()


    def start_suite(self, name, attrs):
        #increment test suite counter
        self.total_test_suites_executed = self.total_test_suites_executed +1
        self.test_suite_name = str(attrs['longname']).split(".")[-1]

    def start_test(self, name, attrs):
        #increment the test case counter
        self.total_test_cases_executed = self.total_test_cases_executed+1
        self.test_case_name = str(attrs['longname']).split(".")[-1]
        global test_script_name
        test_script_name = str(attrs['id'])
        global output_file
        self.outfile = open(output_file, 'a')
        self.outfile2 = open(self.summary_output_file, 'a')
        suite_name = self.test_suite_name
        test_case_name = str(attrs['longname'])
        steps = "Execution started"
        status = ""
        start_time = ""
        end_time = ""
        message = ""
        self.outfile.write("\n<tr><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri id= "+test_script_name+">" + test_case_name + "</td><td align=Center colspan=10 bgcolor=orange><font color='green' size=2 face=Calibri>" + steps + "</td></tr>")
        self.close1()

    def start_keyword(self, name, attrs):
        self.keyword = str(attrs['kwname'])

    def end_keyword(self, name, attrs):
        self.outfile = open(output_file, 'a')
        suite_name = self.test_suite_name
        test_case_name = self.test_case_name
        steps = str(name)
        status = str(attrs['status'])
        start_time = str(attrs['starttime'])
        end_time = str(attrs['endtime'])
        arguments=str(attrs['args'])
        message = ""
        if status == "PASS":
            self.outfile.write("\n<tr><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + arguments + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + end_time + "</td></tr>")
        else:
            self.outfile.write("\n<tr><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + arguments + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + end_time + "</td></tr>")
        self.outfile.close()

    def end_test(self, name, attrs):
        global test_script_name
        if attrs['status'] == 'FAIL':
            self.total_test_cases_failed = self.total_test_cases_failed + 1
        elif attrs['status'] == 'PASS':
            self.total_test_cases_passed = self.total_test_cases_passed + 1
        global output_file
        self.outfile = open(output_file, 'a')
        self.outfile2 = open(self.summary_output_file, 'a')
        suite_name = self.test_suite_name
        test_case_name = str(attrs['longname']).split(".")[-1]
        steps = "Execution ended"
        status = str(attrs['status'])
        start_time = str(attrs['starttime'])
        end_time = str(attrs['endtime'])
        message = str(attrs['message'])
        if status == "PASS":
            self.outfile.write("\n<tr><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + test_case_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + status + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + end_time + "</td></tr>")
            self.outfile2.write("\n<tr><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri><a href ='Detailed_test_case_report.html#"+test_script_name+"'>" + test_case_name + "</a></td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + status + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + end_time + "</td></tr>")
        else:
            self.outfile.write("\n<tr><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + test_case_name + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + status + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + end_time + "</td></tr>")
            self.outfile2.write("\n<tr><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri><a href = 'Detailed_test_case_report.html#"+test_script_name+"'>" + test_case_name + "</a></td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + status + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='red' size=2 face=Calibri>" + end_time + "</td></tr>")
        self.close1()
        self.test_case_name = ""

    def end_suite(self, name, attrs):
        self.test_suite_name = ""

    def log_message(self,message):
        self.outfile = open(output_file, 'a')
        suite_name = self.test_suite_name
        test_case_name = self.test_case_name
        steps = self.keyword
        status = ""
        start_time = ""
        end_time = ""
        message = str(message['message']) + " Log level: " + str(message['level'])
        if 'jpg' in message:
            end_index = message.find(".jpg")
            start_index = message.find('a href="') + len('a href="')
            screenshot_name = message[start_index:end_index]
            global output_dir_path
            message = "<a href = '"+output_dir_path +"/"+screenshot_name+".jpg'><img src='" +output_dir_path +"/"+ screenshot_name + ".jpg' width = '200' height='200'</img></a>"
        self.outfile.write("\n<tr><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + suite_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + test_case_name + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + steps + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + status + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + message + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + start_time + "</td><td align=Center colspan=2><font color='green' size=2 face=Calibri>" + end_time + "</td></tr>")
        self.outfile.close()


    def close(self):
        # pass
        self.update_file("<!--Execution Status", "Execution Completed")

    def close1(self):
        # pass
        self.outfile.close()
        if self.outfile2 is not None:
            self.outfile2.close()
        self.update_stat()

    def update_stat(self):
        # pass
        self.update_file("<!--Total Test Cases", str(self.total_test_cases_executed))
        self.update_file("<!--Total Pass Count", str(self.total_test_cases_passed))
        self.update_file("<!--Total Fail Count", str(self.total_test_cases_failed))
        self.update_file("<!--Total Pending Count", str(self.total_test_cases_executed-self.total_test_cases_passed-self.total_test_cases_failed))
        # self.update_file("<!--Execution Status", str("Execution is In progress.. or Terminated"))

    def update_file(self, str_text, str_value):
        with open(output_file) as f:
        # with open('D:\\Rough\\Detailed_test_case_report.html') as f:
            str1 = f.read()
        str1 = str1[:str1.find(str_text+" s-->") + len(str_text+" s-->")] + str_value + str1[str1.find(str_text+" e-->"):]
        self.outfile = open(output_file, 'w')
        self.outfile.write(str1)
        self.outfile.close

        with open(self.summary_output_file) as f2:
            str1 = f2.read()
        str1 = str1[:str1.find(str_text + " s-->") + len(str_text + " s-->")] + str_value + str1[str1.find(str_text + " e-->"):]
        self.outfile2 = open(self.summary_output_file, 'w')
        self.outfile2.write(str1)
        self.outfile2.close