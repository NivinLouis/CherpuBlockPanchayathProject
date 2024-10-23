import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import mm, inch

st.set_page_config(
    page_title='Cherpu Block Panchayath',
    page_icon='♿️',
    layout='wide',
    initial_sidebar_state='collapsed'
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.logo("assets/logo.png")
st.title(" Care Connect")

def print_pdf():
    # --- LOAD PDF ----
    custom =  (20 * inch, 10 * inch)
    pdf = SimpleDocTemplate("Data\export.pdf", pagesize=custom,topMargin=0.3*inch,bottomMargin=0.2*inch)
    table_data = []

    # adding logo
    logo_data=[]
    logo_path = "assets/logo1.png"
    logo = Image(logo_path,width=1536,height=200)
    logo_data.append(logo)
    table_data.append(columns_selection)
    for i, row in data.iterrows():
        table_data.append(list(row))
    table = Table(table_data)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])

    table.setStyle(table_style)
    pdf_table = []
    pdf_table.append(logo)
    pdf_table.append(table)

    pdf.build(pdf_table)

# --- LOAD DATAFRAME ---
sheet_name = 'Form Responses 1'

@st.cache_data
def load_data(file):
    data = pd.read_excel(file,
                sheet_name=sheet_name,
                usecols='B:CJ',
                header=0)
    return data

if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

container2 = st.container(border=True)
col11, col12, col13 = st.columns([1,3,1])
with col12:
    container = st.container(border=True)
    def creds_entered():
        if st.session_state["user"].strip()=="cherpu@2024" and st.session_state["passwd"].strip()=="cherpu@2024":
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False
            if not st.session_state["passwd"]:
                container.warning("Please enter Password")
            elif not st.session_state["user"]:
                container.warning("Please enter username")
            else:
                container.error("Invalid Username/Password ")

    def authenticate_user():
        if "authenticated" not in st.session_state:
            container.image("assets/login.png")
            container.text('')
            container.text_input(label="Username ",value="",key="user",on_change=creds_entered)
            container.text_input(label="Password ",value="",key="passwd", type="password",on_change=creds_entered)
            container.text(' ')
            container.info('Log In Using You Credentials')
            return False
        else:
            if st.session_state["authenticated"]:
                return True
            else:
                container.image("assets/login.png")
                container.text('')
                container.text_input(label="Username ",value="",key="user",on_change=creds_entered)
                container.text_input(label="Password ",value="",key="passwd", type="password",on_change=creds_entered)
                container.text(' ')
                return False

if authenticate_user():
    uploaded_file = st.file_uploader("Choose a file",type='xlsx')
    if uploaded_file is None:
        st.stop()
    df = load_data(uploaded_file)

    # Convert the column to numeric, forcing errors to NaN
    df['No. of Family Members'] = pd.to_numeric(df['No. of Family Members'], errors='coerce')
    df['Personal Income'] = pd.to_numeric(df['Personal Income'], errors='coerce')
    df['Annual Income'] = pd.to_numeric(df['Annual Income'], errors='coerce')
    df['Ward No'] = pd.to_numeric(df['Ward No'], errors='coerce')


    # --- COLUMN SELECTION ---
    columns_list = df.columns.tolist()
    columns_default=['Name','Age','Phone No','Ward No','Gender','Aadhar Card No','Name of Grama Panchayath','Level of Disability','Category','Religion']

    # --- DATA SELECTION ---
    marital_status= df['Marital Status'].unique().tolist()
    gp= df['Name of Grama Panchayath'].unique().tolist()
    ages=df['Age'].unique().astype(int).tolist()
    ward_no= df['Ward No'].unique().astype(int).tolist()
    ward_no.sort()
    genders= df['Gender'].unique().tolist()
    level_disabilities=df['Level of Disability'].unique().tolist()
    percentage_of_disability= df['Percentage  Disability'].unique().tolist()

    # Additional Filtering Data access
    parental_status = df['Parental Status'].unique().tolist()
    family_members = df['No. of Family Members'].unique().astype(int).tolist()
    medical_certificate = df['Medical Board Certificate'].unique().tolist()
    parental_status=df['Parental Status'].unique().tolist()
    uid_card=df['UID Card'].unique().tolist()
    guardianship_certificate=df['Guardianship Certificate'].unique().tolist()
    continnous_support_for_adl=df['Whether Continuous support for ADL needed'].unique().tolist()

    family_selection=(min(family_members),max(family_members))
    type_of_disabilities = set()
    df['Type of Disability'].apply(lambda x: type_of_disabilities.update([i.strip().lower() for i in str(x).split(',')]))
    type_of_disabilities = sorted(type_of_disabilities)

    disability_selection = type_of_disabilities
    medical_selection = medical_certificate
    parental_selection = parental_status
    uid_card_selection = uid_card
    guardianship_certificate_selection=guardianship_certificate
    continnous_support_for_adl_selection=continnous_support_for_adl

    # Abuses Filtering Data Acess
    violence_status = df['Physical Violence'].unique().tolist()
    source_abuse = df['Source of Abuse'].unique().tolist()
    mental_abuse = df['Mental Abuse'].unique().tolist()
    source_mental_abuse = df['Source of Mental Abuse'].unique().tolist()

    violence_selection = violence_status
    source_selection = source_abuse
    mental_selection = mental_abuse
    source_mental_selection = source_mental_abuse

    # Social Status filtering Data Access
    categories = df['Category'].unique().tolist()
    classifications = df['Classification'].unique().tolist()
    religions = df['Religion'].unique().tolist()
    social_protections = set()
    df['Social Protection\n(Mark checkboxes if yes)'].apply(lambda x: social_protections.update([i.strip() for i in str(x).split(',')]))
    social_protections = sorted(social_protections)

    participations = set()
    df['Participation\n(Mark checkboxes if yes)'].apply(lambda x: participations.update([i.strip() for i in str(x).split(',')]))
    participations = sorted(participations)

    participation_family_y_n = df['Participation in Family Decision'].unique().tolist()
    freedom_personal_decision = df['Freedom for Personnel decision'].unique().tolist()
    categories_selection=categories
    classifications_selection=classifications
    religions_selection=religions
    social_protection_selection=social_protections
    participations_selection=participations
    participations_family_selection=participation_family_y_n
    freedom_selection=freedom_personal_decision

    # Economic Status filtering data acess
    personal_income= df['Personal Income'].unique().astype(int).tolist()
    ownership_assets = df['Ownership of Land'].unique().tolist()
    status_of_accomodation = df['Status of Accommodation'].unique().tolist()
    type_of_house = df['Type of House'].unique().tolist()
    employment_status = df['Employment'].unique().tolist()
    annual_income = df['Annual Income'].unique().astype(int).tolist()
    vocational_assesment_conducted = df['Whether Vocational Assessment conducted'].unique().tolist()
    financial_needs = df['Financial Needs'].unique().tolist()
    personal_income_selection=(min(personal_income),max(personal_income))
    annual_income_selection=(min(annual_income),max(annual_income))

    employement_skills = set()
    df['Employment Skill'].apply(lambda x: employement_skills.update([i.strip() for i in str(x).split(',')]))
    employement_skills = sorted(employement_skills)

    training_needs = set()
    df['Training Needs'].apply(lambda x: training_needs.update([i.strip() for i in str(x).split(',')]))
    training_needs = sorted(training_needs)

    status_of_accomodation_selection = status_of_accomodation
    type_of_house_selection = type_of_house
    employment_status_selection = employment_status
    ownership_assets_selection = ownership_assets
    employement_skills_selection = employement_skills
    financial_needs_selection = financial_needs
    vocational_assesment_conducted_selection = vocational_assesment_conducted
    training_needs_selection = training_needs

    # Education status filtering Data Acess
    education_level = df['Educational Level'].unique().tolist()
    category_of_educational_insitution = df['Category of Educational Institution'].unique().tolist()
    whether_vocation_training_y_n = df['Whether Vocational Training Received'].unique().tolist()

    strain_associated_during_education = set()
    df['Strain Associated Education'].apply(lambda x: strain_associated_during_education.update([i.strip() for i in str(x).split(',')]))
    strain_associated_during_education = sorted(strain_associated_during_education)


    vocational_training_recieved = set()
    df['if VT received,Source'].apply(lambda x: vocational_training_recieved.update([i.strip() for i in str(x).split(',')]))
    vocational_training_recieved = sorted(vocational_training_recieved)

    education_level_selection = education_level
    strain_associated_during_education_selection = strain_associated_during_education
    category_of_educational_insitution_selection = category_of_educational_insitution
    whether_vocation_training_y_n_selection = whether_vocation_training_y_n
    vocational_training_recieved_selection = vocational_training_recieved

    # Health status filtering Data Acess
    are_you_a_member_of_government_institution = df['Are you a member of Govt. Insurance'].unique().tolist()
    received_assistance_from_CMDRF_or_KSSM = df['Have you received assistance from CMDRF / KSSM'].unique().tolist()
    have_you_taken_compulsory_immunisation = df['Have you taken compulsory immunization'].unique().tolist()
    type_of_health_method_you_mainly_adopt = df['What type of health method you mainly adopt'].unique().tolist()
    do_you_regularly_depend_on_medicine_yes_or_no = df['Do you regularly depends on medicine'].unique().tolist()
    in_case_of_children_nutritional_status = df['In case of children, nutritional Status'].unique().tolist()
    any_development_delay_identified = df['Any development delay identified'].unique().tolist()

    mark = set()
    df['If Yes then mark'].apply(lambda x: mark.update([i.strip() for i in str(x).split(',')]))
    mark = sorted(mark)

    recurrent_health_issue = set()
    df['Recurrent health issue'].apply(lambda x: recurrent_health_issue.update([i.strip() for i in str(x).split(',')]))
    recurrent_health_issue = sorted(recurrent_health_issue)

    do_you_experience_any_problem_under_intellectual_capacity = set()
    df['Do you experience any problem'].apply(lambda x: do_you_experience_any_problem_under_intellectual_capacity.update([i.strip() for i in str(x).split(',')]))
    do_you_experience_any_problem_under_intellectual_capacity = sorted(do_you_experience_any_problem_under_intellectual_capacity)

    do_you_have_any_locomotor_problem = set()
    df['Do you face any loco motor problem'].apply(lambda x: do_you_have_any_locomotor_problem.update([i.strip() for i in str(x).split(',')]))
    do_you_have_any_locomotor_problem = sorted(do_you_have_any_locomotor_problem)

    comorbidity = set()
    df['Comorbidity'].apply(lambda x: comorbidity.update([i.strip() for i in str(x).split(',')]))
    comorbidity = sorted(comorbidity)


    are_you_a_member_of_government_institution_selection = are_you_a_member_of_government_institution
    mark_selection = mark
    received_assistance_from_CMDRF_or_KSSM_selection = received_assistance_from_CMDRF_or_KSSM
    have_you_taken_compulsory_immunisation_selection = have_you_taken_compulsory_immunisation
    type_of_health_method_you_mainly_adopt_selection = type_of_health_method_you_mainly_adopt
    do_you_regularly_depend_on_medicine_yes_or_no_selection = do_you_regularly_depend_on_medicine_yes_or_no
    #please take care of recurrent health issues
    type_selection = recurrent_health_issue
    in_case_of_children_nutritional_status_selection = in_case_of_children_nutritional_status
    any_development_delay_identified_selection = any_development_delay_identified
    do_you_experience_any_problem_under_intellectual_capacity_selection = do_you_experience_any_problem_under_intellectual_capacity
    do_you_have_any_locomotor_problem_selection = do_you_have_any_locomotor_problem
    comorbidity_selection = comorbidity

    # Rehabilation needs Data Acess
    the_skill_acquired_in_arts_or_sports_if_any_yes_or_no = df['The skills acquired in arts or Sports, if any'].unique().tolist()
    if_talented_why_not_trained = df['If talented,Why not trained'].unique().tolist()
    professional_course_completed = df['Professional Course completed'].unique().tolist()
    completed_vocational_area = df['Completed Vocational area'].unique().tolist()

    the_assistance_required_to_overcome_the_problem = set()
    df['The assistance required to overcome the problem'].apply(lambda x: the_assistance_required_to_overcome_the_problem.update([i.strip() for i in str(x).split(',')]))
    the_assistance_required_to_overcome_the_problem = sorted(the_assistance_required_to_overcome_the_problem)

    skill_area = set()
    df['Skill area\n(Mark checkboxes if yes)'].apply(lambda x: skill_area.update([i.strip() for i in str(x).split(',')]))
    skill_area = sorted(skill_area)

    non_availability_of_rehabilitation_on_support = set()
    df['Non Availability of rehabilitation support'].apply(lambda x: non_availability_of_rehabilitation_on_support.update([i.strip() for i in str(x).split(',')]))
    non_availability_of_rehabilitation_on_support = sorted(non_availability_of_rehabilitation_on_support)

    the_assistance_required_to_overcome_the_problem_selection =the_assistance_required_to_overcome_the_problem
    the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection =the_skill_acquired_in_arts_or_sports_if_any_yes_or_no
    skill_area_selection =skill_area
    if_talented_why_not_trained_selection =if_talented_why_not_trained
    professional_course_completed_selection =professional_course_completed
    completed_vocational_area_selection =completed_vocational_area
    non_availability_of_rehabilitation_on_support_selection =non_availability_of_rehabilitation_on_support

    #Barriers felt at home Data Acess
    barrier_free_physical_facilities_at_home = df['Barrier free physical facilities at home '].unique().tolist()
    availability_of_disabled_friendly_toilets = df['Availability of Disabled friendly toilets'].unique().tolist()
    whether_family_permit_to_travel_outside = df['Whether family permit to travel outside'].unique().tolist()
    do_you_participate_decision_making_at_home_yes_or_no = df['Do you participate decision making at Home'].unique().tolist()
    if_not_why = df['If Not,Why?'].unique().tolist()
    do_you_go_outside_for_personnel_purpose_yes_or_no = df['Do you outside for personal purpose'].unique().tolist()
    is_your_workplace_differently_abled_friendly = df['Is your workplace differently abled friendly'].unique().tolist()
    whether_the_private_institutions_are_differently_abled = df['Wether the private institutions are differently abled friendly'].unique().tolist()

    if_not_BFE_the_deficiency = set()
    df['If not BFE the deficiency'].apply(lambda x: if_not_BFE_the_deficiency.update([i.strip() for i in str(x).split(',')]))
    if_not_BFE_the_deficiency = sorted(if_not_BFE_the_deficiency)

    if_yes_where_do_you_visit = set()
    df['If Yes, Where do you visit'].apply(lambda x: if_yes_where_do_you_visit.update([i.strip() for i in str(x).split(',')]))
    if_yes_where_do_you_visit = sorted(if_yes_where_do_you_visit)

    if_you_do_not_visit_places_why = set()
    df['if you dont visit places,Why?'].apply(lambda x: if_you_do_not_visit_places_why.update([i.strip() for i in str(x).split(',')]))
    if_you_do_not_visit_places_why = sorted(if_you_do_not_visit_places_why)

    barrier_free_physical_facilities_at_home_selection =barrier_free_physical_facilities_at_home
    if_not_BFE_the_deficiency_selection =if_not_BFE_the_deficiency
    availability_of_disabled_friendly_toilets_selection =availability_of_disabled_friendly_toilets
    whether_family_permit_to_travel_outside_selection =whether_family_permit_to_travel_outside
    do_you_participate_decision_making_at_home_yes_or_no_selection =do_you_participate_decision_making_at_home_yes_or_no
    if_not_why_selection =if_not_why
    do_you_go_outside_for_personnel_purpose_yes_or_no_selection =do_you_go_outside_for_personnel_purpose_yes_or_no
    if_yes_where_do_you_visit_selection =if_yes_where_do_you_visit
    if_you_do_not_visit_places_why_selection =if_you_do_not_visit_places_why
    is_your_workplace_differently_abled_friendly_selection =is_your_workplace_differently_abled_friendly
    whether_the_private_institutions_are_differently_abled_selection =whether_the_private_institutions_are_differently_abled


    def _additional_filter():
            global family_selection,disability_selection,medical_selection,uid_card_selection,parental_selection,continnous_support_for_adl_selection,guardianship_certificate_selection
            with st.expander("Filter"):
                family_selection = st.slider('No.of Family Members',
                                                        min_value=0,
                                                        max_value=max(family_members),
                                                        value=(0,max(family_members)))
                disability_selection = st.multiselect('Type of Disability',
                                                        type_of_disabilities,
                                                        default=type_of_disabilities)
                if disability_selection:
                    disability_selection = [item.lower() for item in disability_selection]
                    
                medical_selection = st.multiselect('Medical Certificate Status',
                                                    medical_certificate,
                                                    default=medical_certificate)
                parental_selection = st.multiselect('Parental Status',
                                                    parental_status,
                                                    default=parental_status)
                uid_card_selection = st.multiselect('UID Card',
                                                    uid_card,
                                                    default=uid_card)
                continnous_support_for_adl_selection = st.multiselect('Continous Support Needed For ADL',
                                                    continnous_support_for_adl,
                                                    default=continnous_support_for_adl)
                guardianship_certificate_selection = st.multiselect('Guardianship Certificate',
                                                    guardianship_certificate,
                                                    default=guardianship_certificate)
                
            with st.expander("Social"):
                global categories_selection,classifications_selection,social_selection,participation_y_n_selection,religions_selection,social_protection_selection,participation_y_n_selection,participations_selection,freedom_selection,participations_family_selection
                categories_selection = st.multiselect('Category',
                                                    categories,
                                                    default=categories)
                classifications_selection = st.multiselect('Classification',
                                                    classifications,
                                                    default=classifications)
                religions_selection = st.multiselect('Religion',
                                                religions,
                                                default=religions)
                social_protection_selection = st.multiselect('Social protections',
                                                    social_protections,
                                                    default=social_protections)
                participations_selection = st.multiselect('Participations',
                                                    participations,
                                                    default=participations)
                participations_family_selection = st.multiselect('Participation in family decision',
                                                    participation_family_y_n,
                                                    default=participation_family_y_n)
                freedom_selection = st.multiselect('Freedom for personal decision',
                                                    freedom_personal_decision,
                                                    default=freedom_personal_decision)
            
            with st.expander("Economic"):
                global personal_income_selection,asset_status_selection,status_of_accomodation_selection,type_of_house_selection,employment_status_selection,annual_income_selection,ownership_assets_selection,employement_skills_selection,financial_needs_selection,vocational_assesment_conducted_selection,training_needs_selection
                personal_income_selection = st.slider('Personal Income',
                                            min_value=0,
                                            max_value=min(personal_income),
                                            value=(0,max(personal_income)))
                status_of_accomodation_selection = st.multiselect('Status Of Accomodation',
                                                    status_of_accomodation,
                                                    default=status_of_accomodation)
                type_of_house_selection = st.multiselect('Type Of House',
                                                    type_of_house,
                                                    default=type_of_house)
                employment_status_selection = st.multiselect('Employment Status',
                                                    employment_status,
                                                    default=employment_status)
            
                annual_income_selection = st.slider('Annual Income',
                                            min_value=0,
                                            max_value=max(annual_income),
                                            value=(0,max(annual_income)))
                ownership_assets_selection = st.multiselect('Ownership Assets',
                                                ownership_assets,
                                                default=ownership_assets)
                employement_skills_selection = st.multiselect('Employement Skilla',
                                                    employement_skills,
                                                    default=employement_skills)
                financial_needs_selection = st.multiselect('Financial Needs',
                                                    financial_needs,
                                                    default=financial_needs)
                vocational_assesment_conducted_selection = st.multiselect('Vocational Assesment conducted',
                                                    vocational_assesment_conducted,
                                                    default=vocational_assesment_conducted)
                training_needs_selection = st.multiselect('Training Needs',
                                                    training_needs,
                                                    default=training_needs)
        # Education Status filtering options
            with st.expander("Education"):
                global education_level_selection,strain_associated_during_education_selection,category_of_educational_insitution_selection,whether_vocation_training_y_n_selection,vocational_training_recieved_selection
                education_level_selection = st.multiselect('Education Level',
                                                    education_level,
                                                    default=education_level)
                strain_associated_during_education_selection = st.multiselect('Strain Associated During Education',
                                                    strain_associated_during_education,
                                                    default=strain_associated_during_education)
                category_of_educational_insitution_selection = st.multiselect('Category of Educational Institution',
                                                category_of_educational_insitution,
                                                default=category_of_educational_insitution)
                whether_vocation_training_y_n_selection = st.multiselect('Vocational Training Recieved',
                                                    whether_vocation_training_y_n,
                                                    default=whether_vocation_training_y_n)
                vocational_training_recieved_selection = st.multiselect('Source of VT',
                                                    vocational_training_recieved,
                                                    default=vocational_training_recieved)
        # Health Status filtering options
            with st.expander("Health"):
                global are_you_a_member_of_government_institution_selection,government_institution_selection,mark_selection,received_assistance_from_CMDRF_or_KSSM_selection,have_you_taken_compulsory_immunisation_selection,type_of_health_method_you_mainly_adopt_selection,do_you_regularly_depend_on_medicine_yes_or_no_selection,type_selection,recurring_ailments_if_any_mention_selection,in_case_of_children_nutritional_status_selection,any_development_delay_identified_selection,do_you_experience_any_problem_under_intellectual_capacity_selection,do_you_have_any_locomotor_problem_selection,comorbidity_selection
                are_you_a_member_of_government_institution_selection = st.multiselect('Member of Govt.Insurance',
                                                    are_you_a_member_of_government_institution,
                                                    default=are_you_a_member_of_government_institution)
                mark_selection = st.multiselect('Type of Insurance',
                                                    mark,
                                                    default=mark)
                received_assistance_from_CMDRF_or_KSSM_selection = st.multiselect('Recieved Assistance from CMDRF or KSSM',
                                                received_assistance_from_CMDRF_or_KSSM,
                                                default=received_assistance_from_CMDRF_or_KSSM)
                have_you_taken_compulsory_immunisation_selection = st.multiselect('Taken compulsary immunization',
                                                    have_you_taken_compulsory_immunisation,
                                                    default=have_you_taken_compulsory_immunisation)
                type_of_health_method_you_mainly_adopt_selection = st.multiselect('Health method mainly adopt',
                                                type_of_health_method_you_mainly_adopt,
                                                default=type_of_health_method_you_mainly_adopt)
                do_you_regularly_depend_on_medicine_yes_or_no_selection = st.multiselect('Regularly Depend on Medicine',
                                                    do_you_regularly_depend_on_medicine_yes_or_no,
                                                    default=do_you_regularly_depend_on_medicine_yes_or_no)
                type_selection = st.multiselect('Recurrent Health Issues',
                                                recurrent_health_issue,
                                                default=recurrent_health_issue)
                in_case_of_children_nutritional_status_selection = st.multiselect('Children nutritional status',
                                                in_case_of_children_nutritional_status,
                                                default=in_case_of_children_nutritional_status)
                any_development_delay_identified_selection = st.multiselect('Development delay identified',
                                                    any_development_delay_identified,
                                                    default=any_development_delay_identified)
                do_you_experience_any_problem_under_intellectual_capacity_selection = st.multiselect('Problem under intellectual capacity',
                                                do_you_experience_any_problem_under_intellectual_capacity,
                                                default=do_you_experience_any_problem_under_intellectual_capacity)
                do_you_have_any_locomotor_problem_selection = st.multiselect('Locomotor Problem',
                                                    do_you_have_any_locomotor_problem,
                                                    default=do_you_have_any_locomotor_problem)
                comorbidity_selection = st.multiselect('Comorbidity',
                                                comorbidity,
                                                default=comorbidity)
                
        # Rehabilation Needs filtering options
            with st.expander("Rehabilation"):
                global the_assistance_required_to_overcome_the_problem_selection,the_assistance_required_to_overcome_the_problem_selection,the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection,skill_area_selection,if_talented_why_not_trained_selection,professional_course_completed_selection,completed_vocational_area_selection,non_availability_of_rehabilitation_on_support_selection
                the_assistance_required_to_overcome_the_problem_selection = st.multiselect('Assistance Required to overcome',
                                                    the_assistance_required_to_overcome_the_problem,
                                                    default=the_assistance_required_to_overcome_the_problem)
                the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection = st.multiselect('Skill acquired in Arts/Sports',
                                                    the_skill_acquired_in_arts_or_sports_if_any_yes_or_no,
                                                    default=the_skill_acquired_in_arts_or_sports_if_any_yes_or_no)
                skill_area_selection = st.multiselect('Skill Area',
                                                    skill_area,
                                                    default=skill_area)
                if_talented_why_not_trained_selection = st.multiselect('Why not trained',
                                                if_talented_why_not_trained,
                                                default=if_talented_why_not_trained)
                professional_course_completed_selection = st.multiselect('Professional Courses completed',
                                                    professional_course_completed,
                                                    default=professional_course_completed)
                completed_vocational_area_selection = st.multiselect('Completed Vocational Area',
                                                    completed_vocational_area,
                                                    default=completed_vocational_area)
                non_availability_of_rehabilitation_on_support_selection = st.multiselect('Non availabilty of rehabitalation support',
                                                    non_availability_of_rehabilitation_on_support,
                                                    default=non_availability_of_rehabilitation_on_support)
                
        # Barriers felt at home filtering options
            with st.expander("Barriers felt"):
                global barrier_free_physical_facilities_at_home_selection,if_not_BFE_the_deficiency_selection,availability_of_disabled_friendly_toilets_selection,whether_family_permit_to_travel_outside_selection,do_you_participate_decision_making_at_home_yes_or_no_selection,if_not_why_selection,do_you_go_outside_for_personnel_purpose_yes_or_no_selection,if_yes_where_do_you_visit_selection,if_you_do_not_visit_places_why_selection,is_your_workplace_differently_abled_friendly_selection,whether_the_private_institutions_are_differently_abled_selection,can_you_give_the_names_of_places_not_differently_adled_friendly_selection,which_are_the_places_that_to_be_converted_friendly_immediately_selection
                barrier_free_physical_facilities_at_home_selection = st.multiselect('Barrier free physical facilities at home',
                                                    barrier_free_physical_facilities_at_home,
                                                    default=barrier_free_physical_facilities_at_home)
                if_not_BFE_the_deficiency_selection = st.multiselect('The deficiency',
                                                    if_not_BFE_the_deficiency,
                                                    default=if_not_BFE_the_deficiency)
                availability_of_disabled_friendly_toilets_selection = st.multiselect('Availability of disabled friendly toilets',
                                                    availability_of_disabled_friendly_toilets,
                                                    default=availability_of_disabled_friendly_toilets)
                whether_family_permit_to_travel_outside_selection = st.multiselect('Whether family permits to travel outside',
                                                    whether_family_permit_to_travel_outside,
                                                    default=whether_family_permit_to_travel_outside)
                do_you_participate_decision_making_at_home_yes_or_no_selection = st.multiselect('Participation in decision making at home',
                                                    do_you_participate_decision_making_at_home_yes_or_no,
                                                    default=do_you_participate_decision_making_at_home_yes_or_no)
                if_not_why_selection = st.multiselect('If not why',
                                                    if_not_why,
                                                    default=if_not_why)

                do_you_go_outside_for_personnel_purpose_yes_or_no_selection = st.multiselect('Go outside for personal purposes',
                                                do_you_go_outside_for_personnel_purpose_yes_or_no,
                                                default=do_you_go_outside_for_personnel_purpose_yes_or_no)
                if_yes_where_do_you_visit_selection = st.multiselect('Where do they visit',
                                                    if_yes_where_do_you_visit,
                                                    default=if_yes_where_do_you_visit)
                if_you_do_not_visit_places_why_selection = st.multiselect('Reasons why not visit places',
                                                    if_you_do_not_visit_places_why,
                                                    default=if_you_do_not_visit_places_why)
                is_your_workplace_differently_abled_friendly_selection = st.multiselect('Workplace DA freindly',
                                                    is_your_workplace_differently_abled_friendly,
                                                    default=is_your_workplace_differently_abled_friendly)
                whether_the_private_institutions_are_differently_abled_selection = st.multiselect('Private institutions DA friendly',
                                                    whether_the_private_institutions_are_differently_abled,
                                                    default=whether_the_private_institutions_are_differently_abled)


    with st.sidebar:
        with st.expander("Display"):
            columns_selection = st.multiselect('Select Columns to Display: ',
                                    columns_list,
                                    default=columns_default,
                                    )
        with st.expander("Basic Filtering"):
            age_selection = st.slider('Age:',
                            min_value=0,
                            max_value=max(ages),
                            value=(0,max(ages)))
            gp_selection = st.multiselect('Grama Panchayath',
                                    gp,
                                    default=gp,
                                )
            percentage_of_disability_selection = st.multiselect('Percentage of Disability ',
                                    percentage_of_disability,
                                    default=percentage_of_disability,
                                )
            gender_selection = st.multiselect('Gender',
                                    genders,
                                    default=genders,
                                    )
            level_selection = st.multiselect('Level of Disability',
                                    level_disabilities,
                                    default=level_disabilities,
                                    )
            marital_selection = st.multiselect('Marital Status ',
                                    marital_status,
                                    default=marital_status,
                                )
            ward_selection = st.multiselect('Ward ',
                                    ward_no,
                                    default=ward_no,
                                    )
        on = st.toggle("Show Advanced Filtering Menu")
        if on:
            _additional_filter()
        st.link_button("Meet Our Team ✨", "https://nae-vast.github.io/about/")
                




    # --- FILTERED DATAFRAME ---


    mask=(df['Age'].between(*age_selection) | df['Age'].isnull())  & \
        (df['Marital Status'].isin(marital_selection)) & \
        (df['Name of Grama Panchayath'].isin(gp_selection)) & \
        (df['Gender'].isin(gender_selection)) & \
        (df['Level of Disability'].isin(level_selection)) &\
        (df['Ward No'].isin(ward_selection) | df['Ward No'].isnull()) &\
        (df['Percentage  Disability'].isin(percentage_of_disability_selection)) & \
        (df['No. of Family Members'].between(*family_selection) | df['No. of Family Members'].isnull()) & \
        (df['Parental Status'].isin(parental_selection)) &\
        (df['UID Card'].isin(uid_card_selection)) &\
        (df['Whether Continuous support for ADL needed'].isin(continnous_support_for_adl_selection)) &\
        (df['Guardianship Certificate'].isin(guardianship_certificate_selection)) &\
        (df['Medical Board Certificate'].isin(medical_selection)) &\
        (df['Type of Disability'].apply(lambda x: any(item in [i.strip().lower() for i in str(x).split(',')] for item in disability_selection))) &\
        (df['Physical Violence'].isin(violence_selection)) &\
        (df['Source of Abuse'].isin(source_selection)) &\
        (df['Mental Abuse'].isin(mental_selection)) &\
        (df['Source of Mental Abuse'].isin(source_mental_selection)) &\
        (df['Category'].isin(categories_selection)) &\
        (df['Classification'].isin(classifications_selection)) &\
        (df['Religion'].isin(religions_selection)) &\
        (df['Social Protection\n(Mark checkboxes if yes)'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in social_protection_selection))) &\
        (df['Participation\n(Mark checkboxes if yes)'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in participations_selection))) &\
        (df['Participation in Family Decision'].isin(participations_family_selection)) &\
        (df['Freedom for Personnel decision'].isin(freedom_personal_decision)) &\
        (df['Ownership of Land'].isin(ownership_assets_selection)) &\
        (df['Personal Income'].between(*personal_income_selection)  | df['Personal Income'].isnull()) & \
        (df['Annual Income'].between(*annual_income_selection)  | df['Annual Income'].isnull()) & \
        (df['Status of Accommodation'].isin(status_of_accomodation_selection)) &\
        (df['Type of House'].isin(type_of_house_selection)) &\
        (df['Employment'].isin(employment_status_selection)) &\
        (df['Whether Vocational Assessment conducted'].isin(vocational_assesment_conducted_selection)) &\
        (df['Employment Skill'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in employement_skills_selection))) &\
        (df['Financial Needs'].isin(financial_needs_selection)) &\
        (df['Training Needs'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in training_needs_selection))) &\
        (df['Educational Level'].isin(education_level_selection)) &\
        (df['Strain Associated Education'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in strain_associated_during_education_selection))) &\
        (df['Category of Educational Institution'].isin(category_of_educational_insitution_selection)) &\
        (df['Whether Vocational Training Received'].isin(whether_vocation_training_y_n_selection)) &\
        (df['if VT received,Source'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in vocational_training_recieved_selection))) &\
        (df['Are you a member of Govt. Insurance'].isin(are_you_a_member_of_government_institution_selection)) &\
        (df['If Yes then mark'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in mark_selection))) &\
        (df['Have you received assistance from CMDRF / KSSM'].isin(received_assistance_from_CMDRF_or_KSSM_selection)) &\
        (df['Have you taken compulsory immunization'].isin(have_you_taken_compulsory_immunisation_selection)) &\
        (df['What type of health method you mainly adopt'].isin(type_of_health_method_you_mainly_adopt_selection)) &\
        (df['Do you regularly depends on medicine'].isin(do_you_regularly_depend_on_medicine_yes_or_no_selection)) &\
        (df['Recurrent health issue'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in type_selection))) &\
        (df['In case of children, nutritional Status'].isin(in_case_of_children_nutritional_status_selection)) &\
        (df['Any development delay identified'].isin(any_development_delay_identified_selection)) &\
        (df['Do you experience any problem'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in do_you_experience_any_problem_under_intellectual_capacity_selection))) &\
        (df['Do you face any loco motor problem'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in do_you_have_any_locomotor_problem_selection))) &\
        (df['Comorbidity'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in comorbidity_selection))) &\
        (df['The assistance required to overcome the problem'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in the_assistance_required_to_overcome_the_problem_selection))) &\
        (df['The skills acquired in arts or Sports, if any'].isin(the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection)) &\
        (df['Skill area\n(Mark checkboxes if yes)'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in skill_area_selection))) &\
        (df['If talented,Why not trained'].isin(if_talented_why_not_trained_selection)) &\
        (df['Professional Course completed'].isin(professional_course_completed_selection)) &\
        (df['Completed Vocational area'].isin(completed_vocational_area_selection)) &\
        (df['Non Availability of rehabilitation support'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in non_availability_of_rehabilitation_on_support_selection))) &\
        (df['Barrier free physical facilities at home '].isin(barrier_free_physical_facilities_at_home_selection)) &\
        (df['If not BFE the deficiency'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in if_not_BFE_the_deficiency_selection))) &\
        (df['Availability of Disabled friendly toilets'].isin(availability_of_disabled_friendly_toilets_selection)) &\
        (df['Whether family permit to travel outside'].isin(whether_family_permit_to_travel_outside_selection)) &\
        (df['Do you participate decision making at Home'].isin(do_you_participate_decision_making_at_home_yes_or_no_selection)) &\
        (df['If Not,Why?'].isin(if_not_why_selection)) &\
        (df['Do you outside for personal purpose'].isin(do_you_go_outside_for_personnel_purpose_yes_or_no_selection)) &\
        (df['If Yes, Where do you visit'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in if_yes_where_do_you_visit_selection))) &\
        (df['if you dont visit places,Why?'].apply(lambda x: any(item in [i.strip() for i in str(x).split(',')] for item in if_you_do_not_visit_places_why_selection))) &\
        (df['Is your workplace differently abled friendly'].isin(is_your_workplace_differently_abled_friendly_selection)) &\
        (df['Wether the private institutions are differently abled friendly'].isin(whether_the_private_institutions_are_differently_abled_selection))

    number_of_result=df[mask].shape[0]
    st.markdown(f'*Available Results:{number_of_result}*')
    data=df[mask][columns_selection].reset_index(drop=True)
    st.dataframe(data,use_container_width=True)

    col1,col2,col3,col4= st.columns([1,3,1,1])

    if col1.button("Export Data",type='primary'):
        with st.spinner('Generating...'):
            print_pdf()
            with open("Data\export.pdf", "rb") as pdf_file:
                        PDFbyte = pdf_file.read()
                        col3.download_button(label="Download PDF",
                                            data=PDFbyte,
                                            file_name="Export.pdf",
                                            mime='application/octet-stream')
                        
                        col4.download_button("Download CSV",
                                        data.to_csv(),
                                        file_name="Export.csv",
                                        mime = 'text/csv')


