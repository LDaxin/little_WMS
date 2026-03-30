class System():

    value_list = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    def up(self, string):
        rString = reversed(string)
        arr = []
        for i in rString:
            arr.append(self.value_list.index(i))

        arr[0] += 1
        for i in range(0 , len(arr)):
            if arr[i] == 36:
                arr[i] = 0
                arr[i+1] += 1
            else:
                break

        for i in range(0, len(arr)):
            arr[i] = self.value_list[arr[i]]

        string = "".join(reversed(arr))


        return string
