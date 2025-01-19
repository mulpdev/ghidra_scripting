# Plugin Tool
tool = state.getTool()

# Follow the GUI tree from Edit > Tool Options
category_name = 'Listing Fields'
option_names = []

# see also Ghidra/Features/Base/src/main/java/ghidra/app/util/viewier/field/BrowserCodeUnitFormatOptions:50-52
option_names.append('Operands Field.Markup Inferred Variable References')
option_names.append('Operands Field.Markup Register Variable References')
option_names.append('Operands Field.Markup Stack Variable References')

# ToolOptions
tool_options = tool.getOptions(category_name)
for option_name in option_names:
    value_obj = tool.options.getObject(option_name, None) # return None if not found
    # Look at Options NOT ToolOptions for this method
    tool_options.setBoolean(option_name, not value_obj)
    print("Set {} {} to {}".format(category_name, option_name, not value_obj))
