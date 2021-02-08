#----------------------------------------------
# Author : Min-Ju Hwang. 2019.10.23
#-----------------------------------------------
import threading

class TextSpliter(threading.Thread):
    def write_split_file(self, count, lines):
        origName = self.src.replace('.txt','') # .txt 빼고 제목 따기
        if self.chkAutoRename:
            path = '/'.join(origName.split('/')[0:-1]) + '/'
            splitName = path + str(lines[0]) + '.txt'  # 제목 뒤에 붙이기
        else:
            splitName = origName + '-' + str(count) + '화.txt' # 제목 뒤에 붙이기

        with open(splitName, 'w', encoding='utf8') as fd:
            fd.write('\ufeff')
            fd.write("\n".join(lines))
            fd.close()
            self.updateLogMsg(splitName.split('/')[-1] + " >>")

    def run(self):
        self.updateLogMsg("====== Text Spliter is Starting ======")
        # limit = int(sys.argv[2])
        lineList = []
        with open(self.src, 'r', encoding='utf-8') as ori_file:
            try :
                for line in ori_file :
                    if self.stopFlag :
                        self.parent.threadCanceled.emit()
                        break

                    line = line.strip()
                    if line.startswith(self.delimeter): # '###' 구분자
                        self.write_split_file(self.startIndex, lineList)
                        lineList = []
                        lineList.append(line.split(self.delimeter)[1])
                        self.startIndex += 1 # 파일마다 1,2,3,4,5... 카운팅
                    else: # 구분자 있는 line은 제외하고 텍스트 추가
                        lineList.append(line)
            except Exception as e:
                print(e)
                self.updateLogMsg(str(e))

        if lineList and not self.stopFlag:
            self.write_split_file(self.startIndex, lineList)

        if not self.stopFlag:
            self.updateLogMsg("====== Blice Spliter is Done ======")
            self.parent.threadFinished.emit()

    def updateLogMsg(self, str):
        self.parent.updateLog.emit(str)

    def thread_stop(self):
        self.stopFlag = True

    def __init__(self, parent, src, delimeter, startIndex, rename=False):
        threading.Thread.__init__(self)
        self.parent = parent
        self.src = src
        self.delimeter = delimeter
        self.startIndex = int(startIndex)
        self.chkAutoRename = rename
        self.stopFlag = False