Sub Button1_Click()
    Dim rng As Range, cell As Range, i As Integer
    Set rng = Range("A:A")
    For Each cell In rng
        If InStr(1, cell.Value, "Date Printed") > 0 Then
            Let delRange = "A" & cell.Row - 3 & ":" & "A" & cell.Row + 2
            Range(delRange).EntireRow.Delete Shift:=xlToUp
        End If
    Next cell
End Sub
