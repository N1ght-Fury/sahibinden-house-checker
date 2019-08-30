import requests
from bs4 import BeautifulSoup
import sys
import time

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

def get_house_details():
	url = 'https://www.sahibinden.com/satilik?address_quarter=23060&address_quarter=23061&address_quarter=23062&address_quarter=23063&address_town=442&a20=38472&price_max=150000&address_city=34'
	soup = get_soup(url)

	house_link = "https://www.sahibinden.com" + str(soup.find('tbody', {'class':'searchResultsRowClass'}).find('tr').td.a['href'])
	title = str(soup.find('tbody', {'class':'searchResultsRowClass'}).find('a', {'class':'classifiedTitle'}).text).replace('\n','').replace('    ','')
	price = str(soup.find('tbody', {'class':'searchResultsRowClass'}).find('td', {'class':'searchResultsPriceValue'}).div.text).replace('\n','').replace(' ','')
	m2 = str(soup.find('tbody', {'class':'searchResultsRowClass'}).find('td', {'class':'searchResultsAttributeValue'}).text).replace('\n','').replace('                    ','')
	date = str(soup.find('tbody', {'class':'searchResultsRowClass'}).find('td', {'class':'searchResultsDateValue'}).span.text)
	neighborhood = "İstanbul / " + "Pendik / " + str(soup.find('tbody', {'class':'searchResultsRowClass'}).find('td', {'class':'searchResultsLocationValue'}).text).replace('\n','').replace('                        ','')
	room = 'Stüdyo (1+0)'

	soup = get_soup(house_link)
	img = soup.find('img',{'class':'stdImg'})['src']

	return [house_link,title,price,m2,date,neighborhood,room,img]

def main_operation():
	while True:
		if (Mail.total_user() == 0):
			print("No user found on database. You have to add at least one user to continue.")
			user_mail = input("Mail: ").lower()

			user_info = user_database.User(user_mail, True)
			Mail.add_mail(user_info)

		try:
			house_details = get_house_details()
			if (not House.check_if_house_exists(house_details[0],house_details[7])):
				New_House = house_database.House(house_details[0],house_details[1],house_details[2],house_details[3],house_details[4],house_details[5],house_details[6],house_details[7])
				House.add_house(New_House)

				mail_list = Mail.get_mails()
				text_mail = text_of_mail.html_text(house_details[0],house_details[1],house_details[2],house_details[3],house_details[4],house_details[5],house_details[6],house_details[7])

				for user in mail_list:
					inform_user.send_mail(user[0], text_mail)

			print('Process finished. Waiting for 3 min.')
			time.sleep(180)

		except Exception as e:
			print('Something unexpected happened. Waiting for 3 min.')
			print(e)
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

			if (user_stat == "Y"):
				user_stat = True
				text = new_mail + " successfully added to database."

			elif (user_stat == "N"):
				user_stat = False
				text = new_mail + " successfully added to database. Be aware that you wont receive any mails."

			else:
				print("\nInvalid command. Try again.\n")
				continue

			new_user = user_database.User(new_mail, user_stat)
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
				"To go back, enter 'q' , to change mail, "
				"enter M, to change status, enter S:")

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