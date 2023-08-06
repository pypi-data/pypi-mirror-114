from pypykatz.registry.aoffline_parser import OffineRegistry
from aiowinreg.ahive import AIOWinRegHive
from aiosmb.commons.interfaces.file import SMBFile
import traceback

async def parse_smbfiles(system_file, sam_file, security_file):
	try:
		po = await OffineRegistry.from_async_reader(system_file, sam_file, security_file)
		await po.get_secrets()
		return po, None

	except Exception as e:
		traceback.print_exc()
		return False, e


async def parse_regfiles_unc(connection, system_unc, sam_unc = None, security_unc = None):
	try:
		security_file = None
		sam_file = None

		system_file = SMBFile.from_uncpath(system_unc)
		_, err = await system_file.open(connection, 'r')
		if err is not None:
			raise err

		if sam_unc is not None:
			sam_file = SMBFile.from_uncpath(sam_unc)
			_, err = await sam_file.open(connection, 'r')
			if err is not None:
				raise err
		
		if security_unc is not None:
			security_file = SMBFile.from_uncpath(security_unc)
			_, err = await security_file.open(connection, 'r')
			if err is not None:
				raise err
		
		return await parse_smbfiles(system_file, sam_file, security_file)

	except Exception as e:
		traceback.print_exc()
		return False, e

	finally:
		await system_file.close()
		if sam_file is not None:
			await sam_file.close()
		
		if security_file is not None:
			await security_file.close()