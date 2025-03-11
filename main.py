from capstoneUpdate import CapstoneUpdate

capstone24 = CapstoneUpdate()
df = capstone24.rest_import()
capstone24.sf()
print(df)
#capstone24.format_focus_areas()
#capstone24.preview_df()
