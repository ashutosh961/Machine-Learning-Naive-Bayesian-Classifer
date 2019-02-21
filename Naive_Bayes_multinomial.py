#1001581542
#ASHUTOSH UPADHYE

import os, copy, random, math
import settings as sett
path = os.path.join(os.getcwd(), "20_newsgroups\\")
import numpy as np



class Naive_Bayes_multinomial:

    def clean_text(self, data):
        data = data.replace('\n', ' ')
        remove_l = ['<','>','?','.','"',')','(','|','-','#','*','+']
        replace_l = ["'",'!','/','\\','=',',',':']
        data = data.lower()
        for i in remove_l:
            data = data.replace(i, '')
        for i in replace_l:
            data = data.replace(i, ' ')
        return data

    def get_file(self):
        global group
        while (len(sett.folder_l)):
            r_fo = random.randint(0,len(sett.folder_l)-1)
            folder_n = sett.folder_l[r_fo]
            if len(sett.file_name[folder_n])== 0:
                sett.folder_l.remove(folder_n)
            else:
                r_fi = random.randint(0, len(sett.file_name[folder_n])-1)
                fil = sett.file_name[folder_n][r_fi]
                sett.file_name[folder_n].remove(fil)
                group = folder_n
                data = open(path + folder_n + '/'+ fil,'r')
                return data.read()
        group = 'NULL'
        return 'NULL'

    def get_probability(self,fields, dictionary):
        sum_ = np.float64(sum(dictionary.values()))
        p = np.float64(0.0)
        for f in fields:
            value = np.float64(dictionary.get(f, 0.0) + 0.001)
            p = np.float64(p) + np.float64(math.log(np.float64(value)/np.float64(sum_)))
        return p

    def test(self,folder_list,dictionary):
        print("Starting testing part....")
        data = 1
        sett.folder_l = copy.deepcopy(folder_list)
        iteration = 0
        accuracy = 0
        while (data):
            data = mnb.get_file()
            iteration = iteration + 1
            if data == 'NULL':
                break
            data = mnb.clean_text(data)
            fields = data.split(' ')
            probabilities = []
            for c in folder_list:
                probabilities.append(mnb.get_probability(fields, dictionary[c]))
            if group == folder_list[probabilities.index(max(probabilities))]:
                accuracy = accuracy + 1
                print(accuracy)
        print('Accuracy = %.1f' % (float(accuracy) / float(iteration - 1) * 100))

    def main(self):
        global path, group

        folder_list = os.listdir(path)
        i = 0
        total_dic = {}
        dictionary = {}
        sett.file_name = {}
        group = 'NULL'
        print("Starting training part....")
        for fo in folder_list:
            dict_label = {}
            folder_ = path + fo
            files = os.listdir(folder_)
            number = 0
            for file in files:
                number += 1
                if number > 500:
                    break
                add = folder_ + '/'+file
                myfile = open(add,'r')
                data = mnb.clean_text(myfile.read())
                word_count = data.split(' ')
                for field in word_count:
                    value_label= dict_label.get(field, 0)
                    value_total = total_dic.get(field, 0)
                    if value_label == 0:
                        dict_label[field] = 1
                    else:
                        dict_label[field] = value_label + 1
                    if value_total == 0:
                        total_dic[field] = 1
                    else:
                        total_dic[field] = value_total + 1
                files.remove(file)
            sett.file_name[fo] = files
            dictionary[fo] = dict_label
        print("Training Complete")
        mnb.test(folder_list,dictionary)

sett.init()
sett.path = os.path.join(os.getcwd(), "20_newsgroups\\")
mnb = Naive_Bayes_multinomial()
mnb.main()