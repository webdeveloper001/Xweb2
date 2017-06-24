from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html
import time
import json
import csv

# fields = {
# 	"355":  "car_postcode", 
# 	"356":  "dealer_name", 
# 	"361":  "car_make", 
# 	"362":  "make_model", 
# 	"383":  "next_image", 
# 	"384":  "next_page", 
# 	"385":  "car_price", 
# 	"418":  "kjhkjh", 
# 	"420":  "next_url"
# }

# data = {
# 	"384": "//ul[contains(@class, 'pagination')]/li[last()]/a", 
# 	"356": "//ul[contains(@class, 'labelicons')]/li[2]/text()", 
# 	"362": "//div[contains(@class, 'col-xs-4')][4]/text()", 
# 	"385": "//h2[contains(@class, 'col-xs-12 col-sm-3 price text-right')]/text()", 
# 	"420": ["//a[contains(@class, 'btn btn-success pull-right')]"]
# }

# data_sq = ["385","362","420 - 0","356","384","355","361","383","420 - 1"]


# REAL CODE


fields = ##FIELD_VALUE##

data = ##DATA_VALUE##

data_sq = ##DATA_SQ_VALUE##

data_urls = ##DATA_URLS_VALUE##

target_dir = '##TARGET_DIR_VALUE##'

display = Display(visible=0, size=(800, 600))
display.start()

def validate(elem): 
	try:
		return elem[0].strip()
	except:
		return ''

s_url = data_urls[data_sq[0]]

# driver = webdriver.PhantomJS() # or add to your PATH
driver = webdriver.Chrome("./chromedriver")
# driver.set_window_size(1024, 768) # optional
driver.set_window_position(0,0)
driver.get(s_url)


all_data = {}
links = []
cur_link = None
nxt_page = False

while True:
	body = html.fromstring(driver.page_source)
	sq_c = 0
	sub_idx = 0
	list_handle = driver.current_window_handle
	while sq_c < len(data_sq):
		idx = data_sq[sq_c]
		if idx.find('-') != -1:
			sub_idx = int(idx.split('-')[-1].strip())
			idx = idx.split('-')[0].strip()
		try:
			all_data[fields[idx]]
		except:
			all_data[fields[idx]] = []
		if fields[idx] == 'next_page':
			try:
				driver.find_element_by_xpath(data[idx]).click()
				nxt_page = True
			except:
				print "Next Page click Failed"
				nxt_page = False
			break
		if fields[idx] == 'next_url':
			print 'next_url processing ' + idx + ' ' + str(sub_idx)
			body = html.fromstring(driver.page_source)

			elems = driver.find_elements_by_xpath(data[idx][sub_idx])

			old_sq_c = sq_c
			pp = 0
			for elem in elems:
				pp = pp + 1
				print fields[idx] + ' started processing'
				print elem
				print driver.current_url

				print driver.window_handles

				webdriver.ActionChains(driver) \
					.key_down(Keys.CONTROL) \
					.click(elem) \
					.key_up(Keys.CONTROL) \
					.perform()

				handles = driver.window_handles

				print handles

				driver.switch_to_window(handles[1])

				sq_c = old_sq_c
				while sq_c < len(data_sq):
					sq_c = sq_c + 1
					idx = data_sq[sq_c]
					xp = data[idx]
					print fields[idx] + ' started sub processing'
					try:
						all_data[fields[idx]]
					except:
						all_data[fields[idx]] = []
					if fields[idx] == 'next_page':
						sq_c = sq_c	- 1
						print 'next_paged breaking'
						break

					else:
						body = html.fromstring(driver.page_source)
						all_data[fields[idx]] += body.xpath(xp)

					print fields[idx] + ' done'

				print fields[idx] + ' done'

				driver.close()
				driver.switch_to_window(handles[0])

				print driver.current_url
		else: 
			all_data[fields[idx]] += body.xpath(data[idx])

		print fields[idx] + ' Done'
		sq_c = sq_c + 1

	if nxt_page == False:
		print 'Done'
		break
	nxt_page = False
	print 'Going to next page'

print all_data

t_data = []

for key in all_data:
	for idx in range(len(all_data[key])):
		try:
			if t_data[idx] is None:
				t_data[idx] = {}
		except:
			t_data.append({})
		t_data[idx][key] = all_data[key][idx]

with open(target_dir + '/result.json', 'w') as f:
	f.write(json.dumps(t_data))
with open(target_dir + '/result.csv', 'w') as f:
	w = csv.writer(f)
	header = all_data.keys()

	header.remove('next_url')
	header.remove('next_page')
	w.writerow(header)
	for row in t_data:
		w.writerow([unicode(item).encode("utf-8") for key, item in row.items()])

driver.close()

display.stop()