import { useEffect, useState } from 'react';
import ProcessInstanceListTable from '../components/ProcessInstanceListTable';
import HttpService from '../services/HttpService';

export default function CompletedInstances() {
  const [userGroups, setUserGroups] = useState<string[] | null>(null);

  useEffect(() => {
    HttpService.makeCallToBackend({
      path: `/user-groups/for-current-user`,
      successCallback: setUserGroups,
    });
  }, [setUserGroups]);

  const groupTableComponents = () => {
    if (!userGroups) {
      return null;
    }

    return userGroups.map((userGroup: string) => {
      const titleText = `This is a list of instances with tasks that were completed by the ${userGroup} group.`;
      return (
        <>
          <h2 title={titleText} className="process-instance-table-header">
            With tasks completed by <strong>{userGroup}</strong>
          </h2>
          <ProcessInstanceListTable
            filtersEnabled={false}
            paginationQueryParamPrefix="group_completed_instances"
            paginationClassName="with-large-bottom-margin"
            perPageOptions={[2, 5, 25]}
            reportIdentifier="system_report_completed_instances_with_tasks_completed_by_my_groups"
            showReports={false}
            textToShowIfEmpty="This group has no completed instances at this time."
            additionalParams={`user_group_identifier=${userGroup}`}
            showActionsColumn
          />
        </>
      );
    });
  };

  const startedByMeTitleText =
    'This is a list of instances you started that are now complete.';
  const withTasksCompletedByMeTitleText =
    'This is a list of instances where you have completed tasks.';

  return (
    <>
      <h2
        title={startedByMeTitleText}
        className="process-instance-table-header"
      >
        Started by me
      </h2>
      <ProcessInstanceListTable
        filtersEnabled={false}
        paginationQueryParamPrefix="my_completed_instances"
        perPageOptions={[2, 5, 25]}
        reportIdentifier="system_report_completed_instances_initiated_by_me"
        showReports={false}
        textToShowIfEmpty="You have no completed instances at this time."
        paginationClassName="with-large-bottom-margin"
        autoReload
        showActionsColumn
      />
      <h2
        title={withTasksCompletedByMeTitleText}
        className="process-instance-table-header"
      >
        With tasks completed by me
      </h2>
      <ProcessInstanceListTable
        filtersEnabled={false}
        paginationQueryParamPrefix="my_completed_tasks"
        perPageOptions={[2, 5, 25]}
        reportIdentifier="system_report_completed_instances_with_tasks_completed_by_me"
        showReports={false}
        textToShowIfEmpty="You have no completed instances at this time."
        paginationClassName="with-large-bottom-margin"
        showActionsColumn
      />
      {groupTableComponents()}
    </>
  );
}
