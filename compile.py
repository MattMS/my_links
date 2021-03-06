import json
import logging
import os


logger = logging.getLogger(__name__)


def get_title_from_file_path(full_path, base_path):
	rel_path = os.path.relpath(full_path, base_path)

	rel_path_no_ext = os.path.splitext(rel_path)[0]

	return rel_path_no_ext.replace(os.sep, ' ')


def split_text(text, sep='='):
	i = text.find(sep)
	return (text[:i], text[i + 1:])


def get_link_from_file(base_path, full_path):
	link = None
	title = None

	logger.debug('Reading file %s', full_path)

	with open(full_path) as r:
		details = dict([split_text(line.strip()) for line in r])

		link = details.get('link')

		if link is not None:
			title = get_title_from_file_path(full_path, base_path)

	return (title, link)


def get_links_from_files(base_path):
	all_links = dict()

	for parent_path, folders, files in os.walk(base_path):
		logger.debug('Reading folder %s', parent_path)

		for file_name in files:
			if '.txt' == os.path.splitext(file_name)[1]:
				full_path = os.path.join(parent_path, file_name)

				title, link = get_link_from_file(base_path, full_path)

				if title is None or link is None:
					continue

				all_links[title] = link

				logger.debug('Added link %s', link)

	return all_links


if '__main__' == __name__:
	logging.basicConfig(level=logging.DEBUG)

	cur_path = os.getcwd()
	links_path = os.path.join(cur_path, 'to')
	json_path = os.path.join(cur_path, 'data.json')

	all_links = get_links_from_files(links_path)

	sorted_names = sorted(all_links.keys(), key=str.lower)

	pairs = [(name, all_links[name]) for name in sorted_names]

	with open(json_path, 'w') as w:
		json.dump(dict(links=pairs), w)
