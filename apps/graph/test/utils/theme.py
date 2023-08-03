import dash_mantine_components as dmc

def themeProvider(content = []):
    return dmc.MantineProvider(
                    id='mantine-provider',
                    withGlobalStyles=True,
                    theme={},
                    inherit=True,
                    children=dmc.Container(content,fluid=True,id='container')
     )

def Container(content=[]):
    return dmc.NotificationsProvider(content)#,fluid=True,id='container'
    
    