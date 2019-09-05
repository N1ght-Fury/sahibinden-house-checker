import requests
from bs4 import BeautifulSoup
import sys
import time
from datetime import datetime
import traceback

import inform_user
import user_database
import house_database
import text_of_mail

House = house_database.Database_Post()
Mail = user_database.Database_User()

def get_soup(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	response = requests.get(url, headers=headers)
	html_content = response.content
	soup = BeautifulSoup(html_content, "html.parser")
	return soup

def get_house_details(url):
	index = [0,2,4]
	soup = get_soup(url)

	house_links = []
	titles = []
	prices = []
	m2 = []
	dates = []
	neighborhoods = []
	rooms = []

	for i in range(3):
		house_links.append("https://www.sahibinden.com" + str(soup.find('tbody', {'class':'searchResultsRowClass'}).find_all('a',{'class':'classifiedTitle'})[i]['href']))
		titles.append(str(soup.find('tbody', {'class':'searchResultsRowClass'}).find_all('a', {'class':'classifiedTitle'})[i].text).replace('\n','').replace('    ',''))
		prices.append(str(soup.find('tbody', {'class':'searchResultsRowClass'}).find_all('td', {'class':'searchResultsPriceValue'})[i].div.text).replace('\n','').replace(' ',''))
		m2.append(str(soup.find('tbody', {'class':'searchResultsRowClass'}).find_all('td', {'class':'searchResultsAttributeValue'})[index[i]].text).replace('\n','').replace('                    ',''))
		date = str(soup.find('tbody', {'class':'searchResultsRowClass'}).find_all('td', {'class':'searchResultsDateValue'})[i].span.text)
		date = date.split(' ')
		dates.append(str(int(date[0])) + " " + str(date[1]))
		neighborhoods.append("İstanbul / " + "Pendik / " + str(soup.find('tbody', {'class':'searchResultsRowClass'}).find_all('td', {'class':'searchResultsLocationValue'})[i].text).replace('\n','').replace('                        ',''))
		rooms.append('Stüdyo (1+0)')

	return [house_links,titles,prices,m2,dates,neighborhoods,rooms]

def main_operation():
	month_in_turkish = {'1':'Ocak', '2':'Şubat', '3':'Mart', '4':'Nisan', '5':'Mayıs', '6':'Haziran', '7':'Temmuz', '8':'Ağustos', '9':'Eylül', '10':'Ekim', '11':'Kasım', '12':'Aralık'}
	
	day = datetime.today().day
	month = datetime.today().month
	todays_date = str(day) + " " + str(month_in_turkish[str(month)])

	while True:
		if (Mail.total_user() == 0):
			print("No user found on database. You have to add at least one user to continue.")
			user_mail = input("Mail: ").lower()
			link = input('Link: ')
			link = "['" + str(link) + "']"

			user_info = user_database.User(user_mail, True, link)
			Mail.add_mail(user_info)

		try:
			mail_list = Mail.get_mails()
			for i in mail_list:

				links = eval(i[2])
				
				for j in links:
					house_details = get_house_details(j)

					for k in range(3):

						if (not House.check_if_house_exists(house_details[0][k] + ':' + i[0]) and house_details[4][k] == todays_date):
							
							soup = get_soup(house_details[0][k])
							
							try:
								img = soup.find('img',{'class':'stdImg'})['src']
							except Exception as e:
								img = 'https://s0.shbdn.com/assets/images/no-image:c63bfbc40fa75b991c3a49ff4457c53e.png'

							New_House = house_database.House(house_details[0][k] + ':' + i[0],house_details[1][k],house_details[2][k],house_details[3][k],house_details[4][k],house_details[5][k],house_details[6][k],img)
							House.add_house(New_House)
							House.add_house(New_House,True)

							text_mail = text_of_mail.html_text(house_details[0][k],house_details[1][k],house_details[2][k],house_details[3][k],house_details[4][k],house_details[5][k],house_details[6][k],img)

							inform_user.send_mail(i[0], text_mail)

			
			todays_day = datetime.today().day

			if (todays_day != day):
				House.clear_posts(str(day))
				day = todays_date

			print('Process finished. Waiting for 3 min.')
			time.sleep(180)

		except Exception as e:
			print('Something unexpected happened. Waiting for 3 min.')
			print(traceback.format_exc())
			time.sleep(180)


def user_operations():
	print("""
		Enter '1' to see all users.
		Enter '2' to add a new user.
		Enter '3' to delete a user.
		Enter '4' to update a user.
		Enter '5' to see total number of users.
		Enter '6' to go back to main menu.
		Enter 'q' to exit the program.
		""")

	while True:

		command = input("\nCommand for mail: ")

		if (command == "1"):
			Mail.show_mails()

		elif (command == "2"):
			print("Enter a new mail address:")
			new_mail = input().lower()

			if (Mail.check_if_mail_exists(new_mail)):
				print("\n" + new_mail, "already exists on database. Please try again.\n")
				continue

			print("Would you want to receive mails? (Y/N):")
			user_stat = input().upper()

			link = input('Link: ')
			link = "['" + link + "']"

			if (user_stat == "Y"):
				user_stat = True
				text = new_mail + " successfully added to database."

			elif (user_stat == "N"):
				user_stat = False
				text = new_mail + " successfully added to database. Be aware that you wont receive any mails."

			else:
				print("\nInvalid command. Try again.\n")
				continue

			new_user = user_database.User(new_mail, user_stat,link)
			Mail.add_mail(new_user)

			print(text)


		elif (command == "3"):

			if (Mail.total_user() == 0):
				print("\nNo user found on database.\n")
				continue

			print("Enter the mail address you want to delete:")
			del_mail = input("Mail: ")

			if (Mail.check_if_mail_exists(del_mail) == 0):
				print("There is not such mail address as " + del_mail + ". Please try again")
				continue

			print("Are you sure you want to delete " + del_mail + "? (Y/N):")
			yes_no = input().upper()

			if (yes_no == "Y"):
				Mail.delete_mail(del_mail)
				print(del_mail, " successfully deleted from database.")

			elif (yes_no == "N"):
				print("Process canceled.")
				continue
			else:
				print("\nInvalid command. Please try again.")


		elif (command == "4"):

			if (Mail.total_user() == 0):
				print("\nNo user found on database.\n")
				continue

			print("Enter the mail address you want to update: ")
			update_mail = input()

			if (Mail.check_if_mail_exists(update_mail) == 0):
				print("There is not such mail address as " + update_mail + ". Please try again")
				continue

			print("What would you want to change? "
				"To go back, enter 'q' , to change mail "
				"enter M, to change status enter S, to change link enter L (you will be asked to enter index number the link you want to delete):")

			change_what = input().upper()

			# Updating User Mail
			if (change_what == "M"):
				new_mail = input("Enter a new mail address: ")
				Mail.update_mail(update_mail, new_mail)
				print(update_mail, "changed to", new_mail + ".")

			# Updating Status (if 0, wont receive mails, else will)
			elif (change_what == "S"):
				print("Would you want to get mails or not? (Y/N)")
				yes_no = input().upper()
				if (yes_no == "Y"):
					Mail.update_stat(update_mail, True)
					print(update_mail, "will now receive mails.")
				elif (yes_no == "N"):
					Mail.update_stat(update_mail, False)
					print(update_mail, "will not receive mails anymore.")
				else:
					print("Wrong command. Please try again.")
					continue
			elif (change_what == 'L'):

				link = str(Mail.get_link(update_mail))
				link = eval(link.replace('(',"").replace('"',"").replace(')',"")[1:len(link)-6])

				print('Add/delete/update? ')
				process = input().upper()

				if (process == 'ADD'):
					new_link = input('Enter link: ')
					link.append(new_link)
					Mail.update_link(str(link),update_mail)
					print('Link added successfully.')

				elif (process == 'DELETE'):
					print(str(link))
					print('Enter index number: ')
					index = int(input('Index: '))
					link.pop(index)
					Mail.update_link(str(link),update_mail)
					print('Link deleted successfully.')

				elif (process == 'UPDATE'):
					print(str(link))
					print('Enter index number: ')
					index = int(input('Index: '))
					new_link = input('Enter link: ')
					link[index] = new_link
					Mail.update_link(str(link),update_mail)
					print('Link updated successfully.')

				else:
					print("Wrong command. Please try again.")
					continue


			elif (change_what == "Q"):
				print("You are back to menu.")

			else:
				print("\nInvalid comamnd. Try again.\n")


		elif (command == "5"):

			total = Mail.total_user()

			if (total != 0):
				print("Total number of users: ", total)
			else:
				print("No user found on database.")

		elif (command == "6"):
			# Going Back to Main Menu
			print("\nYou are on main menu right now.\n")
			break

		elif (command == "q"):
			exit()

		else:
			print("Invalid command. Try again.")

def main():
	if (sys.argv[1] == "1"):
		user_operations()
	elif (sys.argv[1] == "2"):
		main_operation()
	else:
		exit()

if __name__ == '__main__':
	main()
