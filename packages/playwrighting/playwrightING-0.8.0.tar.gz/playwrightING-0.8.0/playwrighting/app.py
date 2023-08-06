from playwright.async_api import (
    async_playwright,
    Error,
    TimeoutError as PlayWrightTimeout,
)
from rich import logging
from textual import events
from textual.app import App
from textual.layouts.grid import GridLayout
from textual.message import Message
from textual.view import View
from textual.widgets import Button, Footer, ScrollView

from playwrighting.accounts import Position
from playwrighting.navigation.login import login


class ATM(App):
    async def on_load(self, event: events.Load) -> None:
        await self.bind("q,ctrl+c", "quit", "Quit")

        self.numbers = ScrollView()
        self.footer = Footer()
        self.position = Position.load()

        def make_button(text: str, style: str) -> Button:
            return Button(text, style=style, name=text)

        dark = "white on rgb(51,51,51)"
        light = "black on rgb(165,165,165)"
        yellow = "white on rgb(255,159,7)"

        self.zero = make_button("0", dark)
        self.position_button = make_button("Update position", light)

    async def on_startup(self, event: events.Startup) -> None:
        layout = GridLayout(gap=(2, 1), gutter=1, align=("center", "center"))
        await self.push_view(View(layout))

        layout.add_column("col", max_size=30, repeat=5)
        layout.add_row("row", max_size=15, repeat=5)
        layout.add_row("footer", max_size=1, repeat=1)
        layout.add_areas(
            position_button="col1,row1",
            zero="col2,row1",
            numbers="col1-start|col5-end,row2-start|row4-end",
            footer="col1,footer",
        )

        layout.place(
            position_button=self.position_button,
            numbers=self.numbers,
            zero=self.zero,
            footer=self.footer,
        )

        await self.numbers.update(str(self.position))

    async def message_button_pressed(self, message: Message) -> None:
        assert isinstance(message.sender, Button)
        button_name = message.sender.name

        if button_name == "Update position":
            await self.numbers.update("Updating position...")

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                try:
                    await login(page)

                    new_position = await Position.create(page)
                    old_position = self.position
                    new_position = (
                        await new_position.update(page)
                        if old_position != new_position
                        else new_position.touch()
                    )
                    self.position = new_position
                    await self.numbers.update(str(self.position))
                    new_position.save()

                except PlayWrightTimeout as e:
                    logging.exception(e)
                except Error as e:
                    logging.exception(e)
                finally:
                    await browser.close()


ATM.run(title="ATM")
