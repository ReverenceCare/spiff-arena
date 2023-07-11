import { useEffect, useState } from 'react';
import HttpService from '../services/HttpService';
import InProgressInstances from './InProgressInstances';

export default function DefaultView() {
  const [userGroups, setUserGroups] = useState<string[] | null>(null);

  useEffect(() => {
    HttpService.makeCallToBackend({
      path: `/user-groups/for-current-user`,
      successCallback: setUserGroups,
    });
  }, [setUserGroups]);

  return <InProgressInstances />;
}
