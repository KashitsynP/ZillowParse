import aiofiles

async def save_data(file_name, mode, data):
    async with aiofiles.open(file_name, mode, encoding='utf-8') as file:
        await file.write(data)
        print(f'File {file_name} was sucсessfully saved!')


async def load_data(filename):
    async with aiofiles.open(filename, 'r', encoding='utf-8') as file:
        print(f'File {filename} was successfully loaded!')
        return await file.read()
