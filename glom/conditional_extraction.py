import glom 

data = {
    "customField": [
        {
            "fieldId": "5f482a5514424210633b6164",
            "fieldLabel": "Organization",
            "valueId": "Physical and Life Sciences",
            "valueLabel": "Physical and Life Sciences"
        },
        {
            "fieldId": "5f4585dd14424210633b6162",
            "fieldLabel": "Brands",
            "valueId": "default",
            "valueLabel": "LLNL"
        },
        {
            "fieldId": "5fa4c4ac8dff831cf540d274",
            "fieldLabel": "Referral Bonus",
            "valueId": "1ae60b83-1db2-455d-b97f-65390a52b76b",
            "valueLabel": "Not applicable"
        },
        {
            "fieldId": "5f4825d673fa282066ed7e62",
            "fieldLabel": "Job Code 1",
            "valueId": "PDS.1",
            "valueLabel": "PDS.1 Post-Dr Research Staff  1"
        },
        {
            "fieldId": "5f48419d14424210633b6167",
            "fieldLabel": "Pre-Placement Medical Exam",
            "valueId": "ed3dc956-39d1-4efc-b9d4-091e1fff2535",
            "valueLabel": "Not applicable"
        },
        {
            "fieldId": "5f48288273fa282066ed7e63",
            "fieldLabel": "Category",
            "valueId": "ac0c24d0-4fe3-4fae-b2cc-b8f2d17dde2d",
            "valueLabel": "Physical Life Sciences"
        }
]
}

if __name__ == "__main__":
    spec = (
        "customField",  # get the outer field
        [glom.Check("fieldLabel", equal_to="Organization", default=glom.SKIP)],  # Check each element of the array
        ["valueLabel"],  # extract the label from each matching object
        glom.T[0]  # get the first one; note: this will raise glom.core.PathAccessError if there is no result
    )
    result = glom.glom(data, spec)
    print(result)
