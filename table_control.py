from PyQt5.QtWidgets import QTableWidgetItem


class TableControl(object):
    def __init__(self, table, content_each_line):
        self.table = table
        self.content_each_line = content_each_line

    @staticmethod
    def _append(table, content_each_line, process):
        table.setRowCount(table.rowCount() + 1)
        for j in range(0, len(content_each_line)):
            item = QTableWidgetItem(str(eval('process.' + content_each_line[j])))
            table.setItem(table.rowCount() - 1,
                          j,
                          item)

    def append(self, process):
        TableControl._append(self.table, self.content_each_line, process)

    def pop(self, process):
        pass
        """
        for i in range(0, self.table.rowCount()):
            print(self.table.item(i, 0).text())
            if self.table.item(i, 0).text() == process.pid:
                # Clear this row
                for j in range(0, len(self.content_each_line)):
                    self.table.setItem(i, j, QTableWidgetItem(""))

                time.sleep(1)

                # Move rows after me
                if i < self.table.rowCount() - 1:
                    for j in range(i + 1, self.table.rowCount()):
                        for k in range(0, len(self.content_each_line)):
                            self.table.setItem(i, j, "")

        """