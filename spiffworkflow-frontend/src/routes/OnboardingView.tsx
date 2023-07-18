import { useEffect, useState } from 'react';
import HttpService from '../services/HttpService';
import InProgressInstances from './InProgressInstances';
import { Onboarding } from '../interfaces';
import MyTasks from './MyTasks';
import { useNavigate } from 'react-router-dom';

export default function OnboardingView() {
  const [onboarding, setOnboarding] = useState<Onboarding | null>(null);

  const navigate = useNavigate();
  
  useEffect(() => {
    HttpService.makeCallToBackend({
      path: `/onboarding`,
      successCallback: setOnboarding,
    });
  }, [setOnboarding]);

  const onboardingElement = () => {
    if (onboarding) {
      if (onboarding.type === "default_view") {
        if (onboarding.value === "my_tasks") {
          return <MyTasks />;
        }
      }
      else if (onboarding.type === "user_input_required" && onboarding.process_instance_id && onboarding.task_id) {
      console.log("HERE");
        navigate(`/tasks/${onboarding.process_instance_id}/${onboarding.task_id}`);
      }
    }
    
    return <InProgressInstances />;
  }

  return onboardingElement();
}
