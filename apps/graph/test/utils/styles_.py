import dash_mantine_components as dmc 

styles_chip = {
    "label": {
        "&[data-checked]": {
            "&, &:hover": {
                "backgroundColor": dmc.theme.DEFAULT_COLORS["indigo"][5],
                "color": "white",
            },
        },
    }
}