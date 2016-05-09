def setChildrenPadding(object, paddingX, paddingY):
    for child in object.winfo_children():
        child.grid_configure(padx = paddingX, pady = paddingY)
