import pickle
import re
import requests

class ServiceNow:
    """
    Represents a ServiceNow instance, with credentials.

    :param instance: ServiceNow instance name. Or full ServiceNow instance URL if your URL does not 
        match '<instance>.service-now.com' pattern.
    :param user: ServiceNow instance account user.
    :param pwd: ServiceNow instance account password.
    :param full_instance_url: Set it to True if you're passing full URL to instance param.
    """

    def __init__(self, instance, user, pwd, full_instance_url=False):
        if not instance[0:8] == 'https://':
            https_instance = f'https://{instance}'
        self.__instance_url = https_instance if full_instance_url else f'{https_instance}.service-now.com'
        self.__credentials = user, pwd
        self.__headers = {"Accept":"application/json"}

    def get_table(self, table, api_version=None, **kwargs):
        """
        Sends a GET request to the specified table. Returns servicenowpy.Table object.

        :param table: The table to retrieve records from.
        :param api_version: API version if API versioning is enabled.
        :param **kwargs: All query parameters to the URL.
        :rtype: servicenowpy.Table
        """

        url = f'{self.__instance_url}/api/now/'
        if api_version:
            url += f'{api_version}/'
        url += f'table/{table}?'

        for k, v in kwargs.items():
            url += f'{k}={v}&'

        url = url[:-1] # Removes unnecessary '?' or '&'

        session = requests.Session()
        session.auth = self.__credentials
        session.headers.update(self.__headers)

        result = []
        
        while url:
            response = session.get(url)

            if response.status_code != 200: 
                print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
                exit()

            data = response.json()
            result.extend(data['result'])

            # Searches for the next page link in the pagination relative links
            try:
                link = response.headers['Link']
                m = re.search(r'(.*),<(.*)>;rel="next', link)
                # Loop ends here with url with value None if pagination were needed
                url = m.group(2) if m else None
            except:
                # Loop ends here if no pagination were needed
                break

        return Table(result)


class Table:
    """
    Represents a ServiceNow API table.

    :param records: Data retrieved by get method of the ServiceNow class.
    :param file: Path of pickle file to load data from.
    """

    def __init__(self, records=None, file=None):
        if file:
            self.load_pickle(file)
        else:
            self.__records = records if records else []

    @property
    def records(self):
        return self.__records

    def to_dict(self):
        data_dict = {}

        for key in self.__records[0].keys(): # For each column of the table
            data_dict[key] = []
            for row in self.__records:
                data_dict[key].append(row[key])

        return data_dict

    def to_pickle(self, file: str):
        """
        Create a serialized data file.

        :param file: Name of the file to be created.
        """

        with open(file, mode='wb') as f:
            pickle.dump(self.__records, f)

    def load_pickle(self, file):
        """
        Load serialized data file.

        :param file: Path to file to be loaded.
        """

        with open(file, mode='rb') as f:
            self.__records = pickle.load(f)