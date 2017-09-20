# Paranuara Challenge

Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired us to build a rest API to provide the desired information.

The government from Paranuara provided two json files (located at resource folder) which give information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet. As the systems are not that evolved yet, thus we need to clean and organise the data.

## Requirements

The government of Paranuara requires a web-based API that returns json with the following endpoints

`/v1/companies/\<index\>/employees`
  Returns all employees for the company represented by index `:index`.

`/v1/people/\<index\>/special-common-friends-with?index_other=\<index_other\>`
  Given 2 people, identified by `\<index1\>` and `\<index2\>`, provides their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.

`/v1/people/<index>/diet-preferences`
  Given a person's `\<index\>`, provides a list of fruits and vegetables they like as `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

The host and port are described later in this document.

## Provided data structure

Government data is organised as follows:

`companies.json`: list of records, structured as
  `index`: integer; a public key used in the API (see below)
  `company`: string; company name

`people.json`: list of records, structured as
  `_id`: string, hashed id (?)
  `index`: integer, public key
  `has_died`: boolean
  `balance`: string, seems a decimal prepended with '$'
  `picture`: string, url
  `age`: integer
  `eyeColor`: string
  `name`: string, a person's name
  `gender`: string, 'male' or 'female'
  `company_id`: integer, foreign key into companies table
  `email`: string, an email
  `phone`: string, a phone number with country, area code and number
  `address`: string, full address (all in USA)
  `about`: string, some bio?
  `registered`: string, like ISO 8601
  `tags`: list of strings
  `friends`: list of records
    `index`: integer, foreign key into this table
  `greeting`: string, already composed for user with some text
  `favouriteFood`: list of string with unique food names

### On food categories

As can be seen, there is no classification for fruits and vegetables. After careful analysis, our ETL team has provided a classification which has been added to the resources folder in `food_classes.json`, as follows:

`food_classes.json`: list of records, structured as
  `food`: string
  `kind`: string, either 'fruit' or 'vegetable'

**Note:** after extended discussions with the Paranuara government and a $12 million survey, it was decided to classify 'cucumber' as vegetable, despite it is technically a fruit.

## Installation

The solution is delivered as a docker container that makes use of installed mongo in host environment.

### Prerequisites

Only for Unix/Linux systems and MAC OS X.

- Install MongoDB in host; the app requires a standard _unsecured_ install on host on port 27017.

- Install [Docker](https://www.docker.com/get-docker)

- Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

- The script assumes shell is `/bin/bash`

With small changes this may work on Windows. This has been tested only on MAC OS X.

### Installation

- Clone this repo

    $ git clone https://github.com/carlosayam/paranuara

- To setup docker image and populate the database, run in shell

    $ install

## Usage

Start `mongod` on standard port (27017). Then run in shell

    $ run

The list of endpoints becomes available at http://localhost:7777/sitemap.

To stop the server, type Ctrl-C in shell.

## Improvements

The company has suggested the following improvements to Paranuara's government for a follow up project:

- It is highly recommended to deploy this API over HTTPS and require authentication for each request.

- Add more endpoints to make the requested API more REST-ful.

- As further enhancement, add content negotiation, so an agent would request a particular version of the API by using an 'Accept' header, removing the need to specify version on the URL and making those URLs version-agnostic.