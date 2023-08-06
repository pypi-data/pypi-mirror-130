import pandas as pd
import time

start = input(
    "\n"
    "\n"
              "-------------------------------------------------------\n"
              "           * 𝒲ℰℒ𝒞𝒪ℳℰ 𝒯𝒪 ℰ𝒜𝒮𝒴 𝒟𝒜𝒯𝒜 ℰ𝒩𝒯ℛ𝒴 *         \n"
              "-------------------------------------------------------\n"
              "                 ༒ cяєατєɒ вy мσɪєɪs ༒                \n"
              "                                                       \n"
              "                     ---!!!!---                        \n"
              "    I have some information please read it carefully   \n"
              "                     ---!!!!---                        \n"
              "              press [ENTER] to Continue   :")

for i in range(8):
        time.sleep(0.3)
        print("\n"
              "\n"
              "\n"
              "\n"
              "⫷ It's my time please wait ⫸\n"
              "           .....           \n")


try:
    row_info = input("\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
            "-----------------------------------------------------------\n"
            "         Welcome To The Row Data Section                   \n"
            "-----------------------------------------------------------\n"
            "                        ◤First◥                           \n"
            "!!-When filling the first row, please leave it by pressing \n"
            "the[SPACE]and fill the rows according to demand in the same\n"
            "                           way !!                          \n"
            "!!-In the Function [Triple] you must put 3 rows which must \n"
            "            Not be decreased or increased.!!               \n"
                          "\n"
            "                press _(ENTER)_ to Continue :")


except:
    print(row_info)
n=time.sleep(0.4)
for i in range(20):
    print("..")
    time.sleep(0.1)


try:
    row_1,row_2,row_3=input("\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
            "-----------------------------------------------------------\n"
            "              Welcome To The Row Data Section              \n"
            "-----------------------------------------------------------\n"
            "                        ◤Secondly◥                        \n"
            "    ! Here is the field to insert row data, focus well !   \n"
            "𝟙-You have three rows that cannot be increased or decreased\n"
            "𝟚-First row, then a[space],then the second row,then [space]\n"
            "then the third row.\n"
            "\n"
            "      For Example ->[NAMES_space_AGES_space_COUNTRYS]<-\n"
            "\n"
            "  HERE YOU CAN ENTER THE ROWS -->>> :").split()
except:
    re=input("\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "_______________________________________________________\n"
             "_______________________________________________________\n"
             "        the way you entered the data failed            \n"
             "                 Please try again                      \n"
             "              ! observing the rules !                  \n"
             "                                                       \n"
             "              If you want to continue                  \n"
             "                       PRESS                           \n"
             "                      [ENTER]            :")
    if re== "":
       quit()
    else:
       quit()

col_info_1=input("\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "\n"
                 "-------------------------------------------------------------\n"
                             "                Welcome To The columns Data Section          \n"
                             "-------------------------------------------------------------\n"
                             " -Here you will fill in the columns and here you can fill in \n"
                             "  an infinity of data.\n"
                             "\n"
                             " -Also, the method of inserting data is as before, with each \n"
                             "  value placed, a space must be made between each value and  \n"
                             "  the other.\n"
                             " -One important thing is that you must make all the columns  \n"
                             "  equal in number and value.\n"
                             "                      press ENTER to countue  :")

first_co = [x for x in input("\n"
                             "\n"
                             "\n"
                             "\n"
                             "\n"
                             "\n"
                             "______________________________________________________________\n"
                             "                     columns Data Section                     \n"
                             "--------------------------------------------------------------\n"
                             "                         ---->[1]<----                        \n"
                             "--------------------------------------------------------------\n"
                             " -Here you can enter the data for the first column in the rules\n"
                             "  we introduced earlier.\n"
                             "\n"
                             " -Make sure to put the same number of values in all columns\n"
                             "\n"
                             "  You can put the data column here --->>").split()]


sec_co = [x for x in input("\n"
                           "\n"
                           "\n"
                           "\n"
                           "\n"
                           "______________________________________________________________\n"
                             "                     columns Data Section                     \n"
                             "--------------------------------------------------------------\n"
                             "                         ---->[2]<----                        \n"
                             "--------------------------------------------------------------\n"
                             " -Here you can enter the data for the first column in the rules\n"
                             "  we introduced earlier.\n"
                             "\n"
                             " -Make sure to put the same number of values in all columns\n"
                             "\n"
                             "  You can put the data column here --->>").split()]
ther_co = [x for x in input("\n"
                            "\n"
                            "\n"
                            "\n"
                            "\n"
                            "______________________________________________________________\n"
                             "                     columns Data Section                     \n"
                             "--------------------------------------------------------------\n"
                             "                         ---->[3]<----                        \n"
                             "--------------------------------------------------------------\n"
                             " -Here you can enter the data for the first column in the rules\n"
                             "  we introduced earlier.\n"
                             "\n"
                             " -Make sure to put the same number of values in all columns\n"
                             "\n"
                             "  You can put the data column here --->>").split()]

try:
    index = [x for x in input("\n"
                              "\n"
                              "\n"
                              "\n"
                              "\n"
                              "-------------------------------------------------------------\n"
                             "                     Data Label Section                      \n"
                             "-------------------------------------------------------------\n"
                             "               Here is the data naming section               \n"
                             "\n"
                             "                          [index]                            \n"
                             "           Here you can name the data, for example\n"
                             "            classify it as alphabets, numbers, etc\n"
                             "-!The most important point is to place the label according to\n"
                             " the number of data contained in the columns!      \n"
                             " \n"
                             " You can put index data here---->>>>:").split()]


    for i in range(10):
        print("\n"
              "\n"
              "\n"
              "\n"
              "\n"
              "......The data is processed.......")
        time.sleep(0.2)

except:
    for i in range(7):
        print("\n"
              "\n"
              "\n"
              "\n"
              "\n"
              "......The data is processed.......")
        time.sleep(0.1)
        print(    "......Without index.......")
        time.sleep(0.2)
    print("\n"
          "\n"
          "\n"
          "\n"
          "\n"
          "______Overlay occurred while placing index data________"
          "\n"
          "\n")
    data = pd.DataFrame({row_1: first_co, row_2: sec_co, row_3: ther_co})
    print(data)

def o():
    try:
        data = pd.DataFrame({row_1: first_co, row_2:sec_co, row_3: ther_co}, index=index)
        print(data)

    except:
        data_re = pd.DataFrame({row_1: first_co, row_2: sec_co, row_3: ther_co})
        print(data_re)
        print("______Overlay occurred while placing index data________")



done = o()


class Triple:
    def __init__(self, names, age, sit):
        self.names = first_co
        self.age = sec_co
        self.sit = done

