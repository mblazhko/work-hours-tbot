from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

retrieve_router = Router(name=__name__)


class MonthRetrieve(StatesGroup):
    month = State()


@retrieve_router.message(Command("retrieve_month_hours_quantity"))
@retrieve_router.message(F.text.casefold() == "retrieve_month_hours_quantity")
async def chose_working_year(message: types.Message, state: FSMContext):
    await state.set_state(MonthRetrieve.month)
    await message.answer(
        text="Введіть номер місяця за який хочете дізнатися кількість\n"
             "відпрацьованих годин та суму зароблених коштів."
    )


@retrieve_router.message(MonthRetrieve.month)
async def count_hours_and_amount(message: types.Message, state: FSMContext):
    await state.clear()

    hours = await get_hours_by_month(message.text)
    amount = await get_amount_by_month(message.text)

    await message.answer(
        f"За {message.text} місяць:\n"
        f"- Відпрацьовано {hours} годин\n"
        f"- Зароблено {amount} євро"
    )