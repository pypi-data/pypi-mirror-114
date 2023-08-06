import asyncio
from concurrent.futures import ProcessPoolExecutor
from pypykatz.pypykatz import pypykatz



#### internal functions! all methods should use parse_regfiles for on-the-fly parsing
def parse_lsass_blocking(lsass_file, lsass_unc):
	try:
		lsass_file.open(lsass_unc, 'rb')
		res = pypykatz.parse_minidump_external(lsass_file)
		lsass_file.close()
		return res, None
	except Exception as e:
		return None, e

async def parse_lsass(machine, lsass_unc):
	try:
		lsass_file = machine.get_blocking_file()
		loop = asyncio.get_event_loop()

		with ProcessPoolExecutor() as process_executor:
			coro = loop.run_in_executor(process_executor, parse_lsass_blocking, lsass_file, lsass_unc)
			res, err = await coro
			
			if err is not None:
				return None, err

		return res, None

	except Exception as e:
		return False, e