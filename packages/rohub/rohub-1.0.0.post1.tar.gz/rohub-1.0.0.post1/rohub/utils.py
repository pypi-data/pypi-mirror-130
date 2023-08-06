import requests
from datetime import datetime, timedelta
import time

from rohub import settings
from rohub import rohub


def valid_to(exp_time, token_type):
    """
    Helper function that calculates expiration time for a token.
    :param exp_time: int -> expiration time in seconds.
    :param token_type: str -> token type.
    """
    if exp_time:
        now = datetime.now()
        return now + timedelta(0, exp_time)
    else:
        print(f'Unable to calculate {token_type} expiration time.')


def is_valid(token_type):
    """
    Function that checks if given token is still valid.
    :param token_type: str -> token type.
    :return: boolean -> True if valid, False otherwise.
    """
    if token_type.lower() == "access":
        if settings.ACCESS_TOKEN_VALID_TO:
            now = datetime.now()
            time_difference = settings.ACCESS_TOKEN_VALID_TO - now
            if time_difference.days < 0:
                return False
            else:
                return True
        else:
            print("Missing information regarding token expiration time. Consider logging again!")
    elif token_type.lower() == "refresh":
        if settings.REFRESH_TOKEN_VALID_TO:
            now = datetime.now()
            time_difference = settings.REFRESH_TOKEN_VALID_TO - now
            if time_difference.days < 0:
                return False
            else:
                return True
        else:
            print("Missing information regarding token expiration time. Consider logging again!")
    else:
        print("Token type not recognized! Supported values are access and refresh.")


def get_request(url, use_token=False):
    """
    Function that performs get request with error handling.
    :param url: str -> url.
    :param use_token: boolean -> if True the token will be passed into headers.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    try:
        if use_token:
            headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
            r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT)
        else:
            r = requests.get(url=url, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            if use_token:
                r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT)
            else:
                r = requests.get(url=url, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def get_request_with_params(url, params):
    """
    Function that performs get request with error handling.
    :param url: str -> url.
    :param params: dict -> dictionary with parameters.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    try:
        r = requests.get(url=url, params=params, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.get(url=url, params=params, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def get_file_request(url, use_token=False, application_type=None):
    """
    Function that performs get request with error handling.
    :param url: str -> url.
    :param use_token: boolean -> if True the token will be passed into headers.
    :param application_type: str -> application type that should be passed in headers.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    try:
        if use_token:
            if application_type:
                headers = {"Authorization": f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}",
                           "Accept": application_type}
            else:
                headers = {"Authorization": f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
            r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT, stream=True)
        else:
            if application_type:
                headers = {"Accept": f"application/{application_type}"}
                r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT, stream=True)
            else:
                r = requests.get(url=url, timeout=settings.TIMEOUT, stream=True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            if use_token:
                r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT, stream=True)
            else:
                if application_type:
                    r = requests.get(url=url, headers=headers, timeout=settings.TIMEOUT, stream=True)
                else:
                    r = requests.get(url=url, timeout=settings.TIMEOUT, stream=True)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def post_request(url, data):
    """
    Function that performs post request with error handling.
    :param url: str -> url.
    :param data: dict -> input data.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    try:
        r = requests.post(url=url, headers=headers, data=data, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=url, headers=headers, data=data, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def post_request_with_file(url, file):
    """
    Function that performs post request for uploading file with error handling.
    :param url: str -> url.
    :param file: str -> path to the zip file.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.post(url=url, headers=headers, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=url, headers=headers, files=files, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def post_request_with_data_and_file(url, file, data):
    """
    Function that performs post request for uploading file with error handling.
    :param url: str -> url.
    :param file: str -> path to the file.
    :param data: dict -> input data.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.post(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def patch_request(url, data):
    """
    Function that perform patch request.
    :param url: str -> url.
    :param data: dict -> input data.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    try:
        r = requests.patch(url=url, headers=headers, data=data, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.patch(url=url, headers=headers, data=data, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def patch_request_with_file(url, data, file):
    """
    Function that perform patch request.
    :param url: str -> url.
    :param data: dict -> input data.
    :param file: str -> path to the file.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.patch(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.patch(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def patch_request_with_file_no_data(url, file):
    """
    Function that perform patch request.
    :param url: str -> url.
    :param file: str -> path to the file.
    :return: Response object -> response.
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.patch(url=url, headers=headers, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.patch(url=url, headers=headers, files=files, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def delete_request(url):
    """
    Function that performs delete request with error handling.
    :param url: str -> url.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    try:
        r = requests.delete(url=url, headers=headers, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.delete(url=url, headers=headers, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def put_request(url, data, use_token=False):
    """
    Function that performs put request with error handling.
    :param url: str -> url.
    :param use_token: boolean -> if True the token will be passed into headers.
    :param data: dict -> input data.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    try:
        if use_token:
            headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
            r = requests.put(url=url, data=data, headers=headers, timeout=settings.TIMEOUT)
        else:
            r = requests.put(url=url, data=data, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            if use_token:
                r = requests.put(url=url, data=data, headers=headers, timeout=settings.TIMEOUT)
            else:
                r = requests.put(url=url, data=data, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def put_request_with_file(url, data, file):
    """
    Function that performs file put request with error handling.
    :param url: str -> url.
    :param data: dict -> input data.
    :param file: str -> path to the file.
    :return: Response object -> response
    """
    r = None   # initialize request as empty
    headers = {'Authorization': f"{settings.TOKEN_TYPE.capitalize()} {settings.ACCESS_TOKEN}"}
    files = {'file': open(file, 'rb')}
    try:
        r = requests.put(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Http error occurred.")
        raise SystemExit(e.response.text)
    except requests.exceptions.ConnectionError:
        try:
            print("Connection error occurred. Trying again...")
            r = requests.post(url=url, headers=headers, data=data, files=files, timeout=settings.TIMEOUT)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred for a second time. Aborting...")
            raise SystemExit(e.response.text)
    except requests.exceptions.Timeout as e:
        print("Timeout. Could not connect to the server.")
        raise SystemExit(e.response.text)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return r


def check_for_status(job_url):
    """
    Helper function that makes a number of retries in order to check
    the status of the request.
    :param job_url: str -> url for the request.
    :return: boolean -> if True the status was validate, False otherwise.
    """
    for retry in range(0, settings.RETRIES):
        time.sleep(settings.SLEEP_TIME)
        job_r = get_request(url=job_url, use_token=True)
        job_content = job_r.json()
        job_status = job_content['status']
        if job_status == "SUCCESS":
            return True
    return False


def get_available_enums():
    """
    Helper function for accessing all available enums in the service.
    :return: JSON -> response with dictionary of all available enums.
    """
    r = get_request(url=settings.API_URL + "enums/")
    if r:
        r_json = r.json()
        return r_json


def get_available_licenses():
    """
    Helper function that acquires all available licenses that can be used in the service.
    :returns list -> list containing all available licenses.
    """
    current_page = 1
    r = get_request(url=settings.API_URL + f"search/licenses/?page={current_page}")
    content = r.json()
    results = [record["identifier"] for record in content["results"]]

    while content["next"] is not None:
        current_page += 1
        r = get_request(url=settings.API_URL + f"search/licenses/?page={current_page}")
        content = r.json()
        results.extend([record["identifier"] for record in content["results"]])
    return results


def search_for_user_id(username):
    """
    Helper function for extracting user_id based on the username.
    :param username: str -> Rohub's username.
    :return: str -> Rohub's user id.
    """
    r = get_request(url=settings.API_URL + "users/")
    if r:
        content = r.json()
        try:
            results = content.get("results")
            while content["next"]:
                r = get_request(url=content["next"])
                content = r.json()
                results.extend(content.get("results"))
            user_id = [result for result in results if result["username"] == username]
            if user_id:
                if len(user_id) != 1:
                    print("More than one user with the same username was found. Be careful, the retrieved"
                          " ID may not be exactly what you were looking for!")
                return user_id[0]["identifier"]
            else:
                print(f"User with username: {username} was not found!")
                return
        except KeyError as e:
            print(e)
            return


def validate_against_different_formats(input_value, valid_value_set):
    """
    Function that validates a value against a set of valid values using different formats for the input
    i.e. capital letters, small letters, title.
    :param input_value: str -> value that has to be checked.
    :param valid_value_set: set -> set of valid values.
    :return: list -> validated value.
    """
    input_variations = {input_value, input_value.capitalize(), input_value.lower(),
                        input_value.upper(), input_value.title()}
    verified_value = list(valid_value_set.intersection(input_variations))
    return verified_value


def does_user_exist(username):
    """
    Helper function for validating if user exists.
    :param username: str -> username.
    :return: user's internal id if exists, None otherwise.
    """
    df = rohub.users_find(search=username)
    try:
        identifier = df[df["username"] == username].identifier
    except KeyError:
        return False
    if len(identifier) == 0:
        return False
    elif len(identifier) == 1:
        return identifier.iloc[0]
    else:
        msg = "Unexpected error: Can't validate if user" \
              " exists. This Username was associated with more than one identifier!"
        raise SystemExit(msg)


def does_organization_exist(organization):
    """
    Helper function for validating if organiation exists.
    :param organization: str -> organization name.
    :return: organization's internal id if exists, None otherwise.
    """
    df = rohub.organizations_find(search=organization)
    try:
        identifier = df[df["organization_id"] == organization].identifier
    except KeyError:
        return False
    if len(identifier) == 0:
        return False
    elif len(identifier) == 1:
        return identifier.iloc[0]
    else:
        msg = "Unexpected error: Can't validate if organization" \
              " exists. This organization was associated with more than one identifier!"
        raise SystemExit(msg)


def does_agent_exist(agent_name, allow_org):
    """
    Helper function for checking if user exists in the system based on the username.
    :param agent_name: str -> username.
    :param allow_org: boolean -> if True organization will also be accepted as potential agent.
    :return: agent's internal id if exists, None otherwise.
    """
    if isinstance(agent_name, dict):
        agent_name = agent_name.get("org_id") or agent_name.get("user_id")
        if not agent_name:
            msg = "Username not found in the input data!" \
                  " Username should be provided as either string, or dictionary that contains " \
                  " user_id or org_id key with username value!"
            raise SystemExit(msg)
    user_id = does_user_exist(username=agent_name)
    if user_id:
        return user_id
    else:
        if allow_org:
            org_id = does_organization_exist(organization=agent_name)
            if org_id:
                return org_id
        return False


def list_validated_agents(agents, allow_org):
    """
    Helper function fo creating a list of validated agents.
    :param agents: list -> list of agents.
    :param allow_org: boolean -> if True organization will also be accepted as potential agent.
    :return: list -> list of validated agents.
    """
    validated_agents = []
    for agent in agents:
        # checking if agent already exist or not
        agent_id = does_agent_exist(agent_name=agent, allow_org=allow_org)
        if agent_id:
            print(f"Agent: {agent} recognized in the system.")
            validated_agents.append(agent_id)
        else:
            # create new external_user/organization
            print(f"Agent for: {agent} does not exist in the system, creating a new one"
                  f" based on the input data...")
            if allow_org:
                agent_id = create_agent(data=agent, user_only=False)
            else:
                agent_id = create_agent(data=agent, user_only=True)
            if agent_id:
                validated_agents.append(agent_id)
    return validated_agents


def create_agent(data, user_only):
    """
    Function for creating an agent (external user or organization).
    :param data: dict -> input data.
    :param user_only boolean -> if True the prompt about missing input values will be shown only for users,
    and not for organization.
    :return: str -> agent_id.
    """
    if not isinstance(data, dict):
        if not user_only:
            msg = """"
            ERROR: incorrect input_data!
            Input data has to be provided as list of dictionaries in case of non-existing agents! Below you can find
            examples of input_data for user and organization.
            EITHER user_id or org_id has to be provided! Rest is optional. Display name will be set to user_id/
            org_id in case it was not provided.
            USER:
            {"user_id":"example_username", "display_name": "example_display_name", "email":"example_email", 
            "orcid_id":"example_orcid_id", "affiliation": "example_affiliation"}
            ORGANIZATION:
            {"org_id":"example_organization_name", "display_name": "example_display_name", 
            "email":"example_email", "organization_url": "example_url", "ror_identifier": "example_ror"}
            """
        else:
            msg = """
            ERROR: incorrect input_data!
            Input data has to be provided as list of dictionaries in case of non-existing agents! Below you can find
            example of input_data for user.
            EITHER user_id has to be provided! Rest is optional. Display name will be set to user_id
            in case it was not provided.
            USER:
            {"user_id":"example_username", "display_name": "example_display_name", "email":"example_email", 
            "orcid_id":"example_orcid_id", "affiliation": "example_affiliation"}
            """
        raise SystemExit(msg)
    if user_only:
        # check and create external user only
        if data.get("user_id"):
            # create new external user
            user_id = data.get("user_id")
            display_name = data.get("display_name", user_id)
            email = data.get("email")
            orcid_id = data.get("orcid_id")
            affiliation = data.get("affiliation")
            return rohub.external_user_add(user_id=user_id, display_name=display_name, email=email,
                                           orcid_id=orcid_id, affiliation=affiliation)
    else:
        # check and create external user or organization.
        if data.get("user_id"):
            # create new external user
            user_id = data.get("user_id")
            display_name = data.get("display_name", user_id)
            email = data.get("email")
            orcid_id = data.get("orcid_id")
            affiliation = data.get("affiliation")
            return rohub.external_user_add(user_id=user_id, display_name=display_name, email=email,
                                           orcid_id=orcid_id, affiliation=affiliation)
        elif data.get("org_id"):
            # create new organization
            org_id = data.get("org_id")
            display_name = data.get("display_name", org_id)
            email = data.get("email")
            org_url = data.get("organization_url")
            ror_id = data.get("ror_identifier")
            return rohub.organization_add(organization_id=org_id, display_name=display_name,
                                          email=email, organization_url=org_url, ror_identifier=ror_id)


