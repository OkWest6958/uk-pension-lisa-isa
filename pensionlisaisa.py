import streamlit as st
import numpy as np
import numpy_financial as npf
import pandas as pd
import copy



page_title = "Should I use a pension, LISA, or ISA to save for retirement?"


st.set_page_config(
    page_title=page_title,
    page_icon=":money_with_wings:",
    menu_items={
        'Report a Bug': 'mailto:ok_west_6958@proton.me?subject=Issue%20with%20' + page_title.replace(" ","%20") + '%20app'
        }
)



st.write('# '+page_title)



with st.expander('How to use this calculator'):
    """This calculator is for determining which savings vehicle might be best to utilise
    if you have disposable monthly income that you want to put towards retirement
    \nImportantly this is not a traditional pension forecast tool like you might 
    have used [here](https://www.pensionbee.com/pension-calculator). If you have not used a pension 
    forecast tool before then you should probably start there  
    \nThis calculator is for analysing how valuable it might be to put *additional* 
    money aside on a monthly basis, beyond what you may already be contributing via a workplace pension 
    \nFor example, putting an additional :green[£100] a month into an ISA earning :green[5%] for :green[20] years 
    would allow you to withdraw an additional :green[£271.26] a month over the course of a :green[20] year retirement. 
    This would be in addition to any existing retirement funds such as a workplace pension
    \nIf you are not already opted into your workplace pension and receiving the maximum employer contribution, 
    this is almost certainly the most valuable thing you can do. This calculator will not consider additional employer 
    contributions
    \nUnless you are on a salary sacrifice (SS) workplace pension scheme, a [SIPP](https://www.moneysavingexpert.com/savings/cheap-sipps/) 
    is normally easier to manage and cheaper than 
    a workplace scheme for additional contributions. This calculator will assume any non-SS pensions are SIPPs. This may be relevant as some workplace pension 
    schemes use qualifying earnings which can lead to confusion when attempting alter monthly contributions 
    \nYou will be asked whether you are currently a basic rate or higher rate tax payer, and whether you expect to be a basic rate 
    or higher rate tax payer in retirement. This is used to calculate tax on pension contributions and withdrawals. Note this means 
    if you are e.g. currently an additional rate tax payer, or e.g. below BRT in retirement (perhaps by retiring before state pension age and 
    your existing workplace pension not taking you above the personal tax allowance), this calculator may not be appropriate for you. However in both these 
    scenarios this will give a greater advantage to the pension which is likely the winning option already 
    \nThis calculator is not suitable for comparing additional contributions to a defined benefit pension
    \nPensions, LISAs, and ISAs have many differences in regards to how you contribute to them and how you withdraw from them. 
    The Reddit r/UKPersonalFinance [wiki](https://ukpersonal.finance/isa-vs-lisa-vs-pension/) explains these differences well. 
    It is important that you are familiar with these differences. For example if you need funds before age 55, then a pension or LISA will be unsuitable. 
    Likewise if you need a sizeable fund that will not be covered by a 25% pension lump sum (such as any remaining 
    mortgage balance), then again a pension may not be suitable"""

st.divider()

"""# Monthly deposits"""


brt_tax_rate = 0.2
hrt_tax_rate = 0.4
brt_ni_rate = 0.08
hrt_ni_rate = 0.02

retirement_vehicles = ['pension','LISA','ISA']




include_lisa = st.toggle(
    'Include LISA in comparisons?',
    1,
    help="""LISAs may not be available to open or contribute to, so toggle here to exclude LISAs from any analysis. 
    For example you may be over the age limit to open/contribute, or you may have already used your yearly LISA allowance"""
)



lisa_reminder = ['green', 'included'] if include_lisa else ['red','excluded']    

st.write(
    """:{0[0]}[LISAs {0[1]}]""".format(lisa_reminder)
    )




monthly_deposit = st.number_input(
    'How much do you have per month to save? (£)',
    1,
    100000,
    200,
    help="""How much of your **net** monthly income can you afford to save each month? 
    Don't worry about accounting for pension tax relief or the LISA bonus, this is done automatically"""
)

if monthly_deposit > 333.33 and include_lisa:
    st.warning(
        """Saving this much per month would take you over the yearly LISA deposit limit. 
        It may be beneficial to review the results when saving £333 (to not breach the LISA limit) 
        to see if the LISA is valuable for this amount, and then reuse the calculator for any remaining additional 
        deposits. \n\n For example, use the calculator for £333, then use the calculator again for your remaining £{0:,}
        \n\nThe calculator will display LISA results for the amount you have entered (£{1:,}) which could be misleading""".format(monthly_deposit - 333,monthly_deposit))

salary_sacrifice = st.radio(
    'Do you have access to a salary sacrifice pension?',
    ['Yes', 'No'],
    help="""A salary sacrifice pension scheme allows you to save on national insurance in addition to the tax savings available in a SIPP. 
    This means you can accumulate more into your retirement fund at the same net cost to your monthly disposable income"""
)

tax_bands = ['BRT', 'HRT']

current_tax = st.radio(
    'Are you currently a Basic Rate Tax (BRT) payer or Higher Rate Tax (HRT) payer?',
    tax_bands,
    index=1,
    help="""This is to determine what level of tax relief any pension contributions will get. 
        If you are only just over the HRT threshold, it may be more complicated to work out 
        whether your contributions would have been taxed at the higher rate. You may need 
        to use this calculator once for any contributions that would have been HRT, and 
        again for any contributions that would have been BRT. If you are neither then this calculator will not be suitable for you"""
)

retirement_tax = st.radio(
    'Do you expect to be a Basic Rate Tax (BRT) payer or Higher Rate Tax (HRT) payer in retirement?',
    tax_bands,
    help="""Based on other retirement funds, such as your existing workplace pension and the state pension, 
        you will likely already be above the BRT threshold. You may also expect to be above the HRT threshold 
        depending on how large your existing funds are. Note that it is often possible to tactically withdraw 
        from your pension to remain below the HRT threshold. As such only select HRT if you are certain any additional 
        contributions would definitely be taxed at HRT in retirement. This calculator will not show results for if you will be below 
        the BRT threshold or above the additional rate threshold"""
)

if retirement_tax == 'HRT' and current_tax == 'BRT':
    st.warning("""You have selected that your are currently a BRT and expect to be a HRT in retirement. This is quite unlikely but 
            can happen if for example you have reduced your hours or salary after already accumulating a large pension fund""")


retirement_age = st.number_input(
    'In how many years do you intend to retire? (years)',
    1,
    100,
    20,
    help="""For example if you are age 38 now and intend to retire age 58, you would enter 20 years"""
)

if retirement_age <= 10 and include_lisa:
    st.warning(
        '''You have entered {0} years until retirement and also selected to include LISAs in this analysis. As LISAs 
        can only be drawn down from after age 60 (without penalty), and can only be contributed to before age 50, a time to retirement of {0} years 
        means you would not be able to contribute to a LISA. You can still view the results of this analysis including LISAs, but this may 
        not be helpful to you, and you will not be able to view a more in depth breakdown of the LISA results. This analysis will 
        not consider the LISA early withdrawal penalty'''.format(retirement_age)
    )
elif retirement_age <= 20 and include_lisa:
    st.warning(
        '''You have entered {0} years until retirement and also selected to include LISAs in this analysis. As LISAs 
        can only be drawn down from after age 60 (without penalty), and an account can only be opened before age 40, you should 
        ensure you are able to open a LISA and then decide whether to include them in this analysis. This analysis will not consider the 
        LISA early withdrawal penalty'''.format(retirement_age)
    )   


growth_rate = st.number_input(
    'What rate of return do you think you will get on your retirement fund investments? (%)',
    0.0,
    100.0,
    5.0,
    0.1,
    help="""Your retirement funds will/should be invested in the stock market. To get meaningful results 
    you will need to assume some annual rate of return. [PensionBee](https://www.pensionbee.com/pension-calculator) quote 3%/
    5%/8% as low/medium/high growth. Setting the rate to 0% may not be very realistic, but does highlight the power of 
    tax relief, so you may find this interesting to view"""
)

with st.expander('Why can I not enter different rates of return for different accounts?'):
    """Pensions, LISAs, and ISAs are all just account wrappers which you use to then invest in assets. 
    It is these assets which generate a return, not the account itself
    \nThe choice of account should not significantly impact the expected rate of return of the investments held within it
    \nIf you really want to test different returns from different accounts (because you are concerned about fees for example), 
    you will need to use the calculator for each rate of return and note and compare the results yourself"""

    



if current_tax == 'BRT' and salary_sacrifice == 'Yes':
    pension_monthly_net_deposit = monthly_deposit / (1 - brt_tax_rate - brt_ni_rate)
elif current_tax == 'BRT' and salary_sacrifice == 'No':
    pension_monthly_net_deposit = monthly_deposit / (1 - brt_tax_rate)
elif current_tax == 'HRT' and salary_sacrifice == 'Yes':
    pension_monthly_net_deposit = monthly_deposit / (1 - hrt_tax_rate - hrt_ni_rate)
else:
    pension_monthly_net_deposit = monthly_deposit / (1 - hrt_tax_rate)





lisa_monthly_deposit = monthly_deposit * 1.25


retirement_fvs = -npf.fv(
    growth_rate / 100 / 12,
    retirement_age * 12,
    [pension_monthly_net_deposit,lisa_monthly_deposit,monthly_deposit],
    0
)




st.divider()

"""# Retirement withdrawals"""



with st.expander('Retirement options'):
    retirement_monthly_withdrawal = st.number_input(
        'Desired net monthly withdrawal in retirement? (£)',
        1,
        100000,
        monthly_deposit,
        help="""Must be greater than your pre-retirement monthly deposits, otherwise you would be able to draw down forever even with 0 growth"""
    )

    if retirement_monthly_withdrawal < monthly_deposit:
        st.warning("""You have entered a monthly withdrawal amount less than what you originally contributed, 
                this means you could sustain your withdrawals indefinitely regardless of the growth. You may 
                find you get more meaningful results if you consider withdrawing as much or more than 
                you originally contributed""")

    retirement_growth_rate = st.number_input(
        'Expected rate of return in retirement? (%)',
        0.0,
        100.0,
        growth_rate,
        0.1,
        help="It is common to move to lower risk assets in retire, so typically you would expect a lower rate of return in retirement"
    )

    if retirement_growth_rate > growth_rate:
        st.warning("""You have entered a growth rate in retirement greater than what was expected before retirement. 
            It is common to move to lower risk assets in retirement, so typically you would expect a lower rate of return in retirement""")

    retirement_duration = st.number_input(
        'How long do you expect to be drawing down funds in retirement? (years)',
        1,
        100,
        retirement_age
    )





if retirement_tax == 'BRT':
    pension_monthly_net_withdrawal = retirement_monthly_withdrawal / (1 - 0.75 * brt_tax_rate)
else:
    pension_monthly_net_withdrawal = retirement_monthly_withdrawal / (1 - 0.75 * hrt_tax_rate)






retirement_withdrawal_durations = abs(npf.nper(
    retirement_growth_rate / 100 / 12,
    [-pension_monthly_net_withdrawal,-retirement_monthly_withdrawal,-retirement_monthly_withdrawal],
    retirement_fvs
))



"""When you retire, you could have accumulated (in addition to other existing pensions/funds):"""

for idx, i in enumerate(retirement_fvs):
    if (not include_lisa) and idx == 1:
        pass
    else:
        st.write("\n* :green[£{:,.2f}] in your {}".format(i,retirement_vehicles[idx]))




st.write(
    """In order to receive :green[£{:,.2f}] net per month in retirement from these additional funds, you would need to withdraw:""".format(retirement_monthly_withdrawal))
st.write("""\n* :green[£{:,.2f}] a month from your pension""".format(pension_monthly_net_withdrawal))

if include_lisa:
    st.write("""\n* :green[£{:,.2f}] a month from your LISA""".format(retirement_monthly_withdrawal))

st.write("""\n* :green[£{:,.2f}] a month from your ISA""".format(retirement_monthly_withdrawal))





st.write("This means you could receive :green[£{:,.2f}] net a month (assuming your fund grows at :green[{:,.2f}%]) for:".format(retirement_monthly_withdrawal,retirement_growth_rate))

for idx, i in enumerate(retirement_withdrawal_durations):
    if (not include_lisa) and idx == 1:
        pass
    elif np.isnan(retirement_withdrawal_durations[idx]):
        st.write("\n* :green[Forever] from your {}".format(retirement_vehicles[idx]))
    else:
        st.write("\n* :green[{:.0f} years] and :green[{:.0f} months] from your {}".format(retirement_withdrawal_durations[idx] // 12,retirement_withdrawal_durations[idx] / 12 % 1 * 12, retirement_vehicles[idx]))



retirement_withdrawal_pmt = -npf.pmt(
    retirement_growth_rate / 100 / 12,
    retirement_duration * 12,
    retirement_fvs
)



retirement_withdrawal_pmt[0] = retirement_withdrawal_pmt[0] * 0.25 + retirement_withdrawal_pmt[0] * 0.75 * ((1 - brt_tax_rate) if retirement_tax == 'BRT' else (1-hrt_tax_rate))



st.write("Alternatively, by withdrawing consistently for exactly :green[{:.0f} years] you could be receiving:".format(retirement_duration))

for idx, i in enumerate(retirement_withdrawal_durations):
    if (not include_lisa) and idx == 1:
        pass
    else:
        st.write("\n* :green[£{:,.2f}] a month from your {}".format(retirement_withdrawal_pmt[idx], retirement_vehicles[idx]))


st.divider()

"""# Detailed breakdown"""




accumulation_months = np.arange(retirement_age * 12) + 1

accumulation_df = pd.DataFrame(
    {
        'Month': accumulation_months,
        'Growth': growth_rate,
        'Net take home': -monthly_deposit,
        'Pension deposit': pension_monthly_net_deposit,
        'LISA deposit': lisa_monthly_deposit,
        'ISA deposit': monthly_deposit
    }
)

accumulation_df['Pension fund'] = -npf.fv(
    growth_rate / 100 / 12,
    accumulation_df['Month'],
    accumulation_df['Pension deposit'],
    0
)

accumulation_df['LISA fund'] = -npf.fv(
    growth_rate / 100 / 12,
    accumulation_df['Month'],
    accumulation_df['LISA deposit'],
    0
)

accumulation_df['ISA fund'] = -npf.fv(
    growth_rate / 100 / 12,
    accumulation_df['Month'],
    accumulation_df['ISA deposit'],
    0
)


drawdown_months = np.arange(retirement_duration * 12) + 1


drawdown_df = pd.DataFrame(
    {
        'Month': drawdown_months + retirement_age * 12,
        'Growth': retirement_growth_rate,
        'Net take home': retirement_monthly_withdrawal,
        'Pension deposit': -pension_monthly_net_withdrawal,
        'LISA deposit': -retirement_monthly_withdrawal,
        'ISA deposit': -retirement_monthly_withdrawal
    }
)

drawdown_df['Pension fund'] = -npf.fv(
    retirement_growth_rate / 100 / 12,
    drawdown_df['Month'] - retirement_age * 12,
    drawdown_df['Pension deposit'],
    retirement_fvs[0]
)


drawdown_df['LISA fund'] = -npf.fv(
    retirement_growth_rate / 100 / 12,
    drawdown_df['Month'] - retirement_age * 12,
    drawdown_df['LISA deposit'],
    retirement_fvs[1]
)

drawdown_df['ISA fund'] = -npf.fv(
    retirement_growth_rate / 100 / 12,
    drawdown_df['Month'] - retirement_age * 12,
    drawdown_df['ISA deposit'],
    retirement_fvs[2]
)


schedule_df = pd.concat([accumulation_df,drawdown_df])


if not include_lisa:
    schedule_df.drop(columns=['LISA deposit', 'LISA fund'], inplace=True)




tab1, tab2, tab3, tab4 = st.tabs(['Accumulation/drawdown schedule','Pension','LISA','ISA'])




line_chart_columns = ['Pension fund','LISA fund', 'ISA fund'] if include_lisa else ['Pension fund','ISA fund']

with tab1:

    st.line_chart(schedule_df,x='Month', y=line_chart_columns)

    'If you do not understand the accumulation/drawdown figures shown, please read the other "Detailed breakdowns"'

    with st.expander('Show table'):

        show_growth = st.toggle(
            'Show monthly fund investment returns?',
            help='''Will show the expected returns for a given month based on the size of the fund and
                the expected rate(s) of return. This could be helpful for determining whether the fund is 
                self sustaining (as desired when following the "4% rule" for example)'''
        )

        schedule_df_column_config = {
            "Net take home": st.column_config.NumberColumn(help="""Amount taken/received net to you per month (will be negative when 
                                                           saving for retirement and positive when withdrawing)"""),
        }

        for i in list(schedule_df):
            if i == 'Month':
                pass
            elif i == 'Net take home':
                schedule_df_column_config[i] = st.column_config.NumberColumn(help="""Amount taken/received net to you per month (will be negative when 
                                                           saving for retirement and positive when withdrawing)""")
            elif "deposit" in i:
                schedule_df_column_config[i] = st.column_config.NumberColumn(help="""Amount which will be deposited/withdrawn from the fund by month""")
            elif "fund" in i:
                schedule_df_column_config[i] = st.column_config.NumberColumn(help="""Total value of the fund by month (including growth)""")
            else:
                schedule_df_column_config[i] = st.column_config.NumberColumn(help="""How much the fund generated each month based on it's value and the expected rate of return""")


        if show_growth:
            config_help_message = st.column_config.NumberColumn(help="""How much the fund generated each month based on it's value and the expected rate of return""")
            schedule_df['Pension fund month returns'] = schedule_df['Pension fund'] * schedule_df['Growth'] / 100 / 12
            schedule_df_column_config['Pension fund month returns'] = config_help_message
            if include_lisa:
                schedule_df['LISA fund month returns'] = schedule_df['LISA fund'] * schedule_df['Growth'] / 100 / 12
                schedule_df_column_config['LISA fund month returns'] = config_help_message
            schedule_df['ISA fund month returns'] = schedule_df['ISA fund'] * schedule_df['Growth'] / 100 / 12
            schedule_df_column_config['ISA fund month returns'] = config_help_message
            schedule_df.drop(columns=['Growth'], inplace=True)
            st.dataframe(
                schedule_df.set_index('Month')\
                .style.format('£{:,.2f}'),
                column_config=schedule_df_column_config
            )
        else:
            schedule_df.drop(columns=['Growth'], inplace=True)
            st.dataframe(
                schedule_df.set_index('Month')\
                .style.format('£{:,.2f}'),
                column_config=schedule_df_column_config
            )






with tab2:


    if current_tax == 'BRT':
        current_tax_const = ["basic rate", brt_tax_rate, brt_ni_rate]
    else:
        current_tax_const = ["higher rate", hrt_tax_rate, hrt_ni_rate]

    if retirement_tax == 'BRT':
        retirement_tax_const = ['basic rate',brt_tax_rate]
    else:
        retirement_tax_const = ['higher rate',hrt_tax_rate]




    def detailedexplanationsipp():
        st.write(
            """You are currently a :green[{0}] tax payer so pay :red[{1:.0f}%] tax
            """.format(current_tax_const[0],current_tax_const[1] * 100))
        st.write(
            """Depositing :green[£{:,.2f}] into your SIPP will result in :green[£{:,.2f}] being 
            added in total due to tax relief""".format(monthly_deposit,
                                            pension_monthly_net_deposit)
        )
        if current_tax == 'HRT':
            st.warning("""(As a :green[{}] tax payer, only the first :green[£{:,.2f}] will be automatically added to your SIPP, 
            the remaining :green[£{:,.2f}] will need to be reclaimed manually from HMRC)""".format(current_tax_const[0],
                                                                                    monthly_deposit * 0.25,
                                                                                    pension_monthly_net_deposit - monthly_deposit - monthly_deposit * 0.25))
        st.write(
        """You expect to be a :green[{}] tax payer in retirement, so will pay :red[{:,.0f}%] tax. 
        You do not pay national insurance on pension drawdown""".format(retirement_tax_const[0],
                                                                        retirement_tax_const[1] * 100)
        )
        st.write(
            """To take home :green[£{:,.2f}] net from you pension, you would need to withdraw :green[£{:,.2f}]""".format(retirement_monthly_withdrawal, 
                                                                                                            pension_monthly_net_withdrawal)
        )
        st.write(
            """(Of your :green[£{:,.2f}] withdrawal, 25% (:green[£{:,.2f}]) can be taken tax free, and 
            the remaining 75% (:green[£{:,.2f}]) is taxed as income (:red[£{:,.2f}] taken as tax leaving :green[£{:,.2f}] after tax). 
            This totals :green[£{:,.2f}] net take home)""".format(pension_monthly_net_withdrawal,
                                                            pension_monthly_net_withdrawal * 0.25,
                                                            pension_monthly_net_withdrawal * 0.75,
                                                            pension_monthly_net_withdrawal * 0.75 * retirement_tax_const[1],
                                                            pension_monthly_net_withdrawal * 0.75 * (1 - retirement_tax_const[1]),
                                                            retirement_monthly_withdrawal)
        )

        

    def detailedexplanationss():
        st.write(
            """You are currently a :green[{0}] tax payer so pay :red[{1:.0f}%] tax and :red[{2:.0f}%] national insurance
            """.format(current_tax_const[0],current_tax_const[1] * 100, current_tax_const[2] * 100))
        st.write(
            """Giving up :green[£{:,.2f}] of your net income would result in :green[£{:,.2f}] being 
            deposited into your pension""".format(monthly_deposit,pension_monthly_net_deposit)
        )
        st.write(
            """(:green[£{:,.2f}] of gross pay would normally incur :red[£{:,.2f}] in tax and :red[£{:,.2f}] in national insurance, 
            resulting in :green[£{:,.2f}] net income. By salary sacrificing, all gross pay goes towards your pension)""".format(pension_monthly_net_deposit,
                                                                                                                pension_monthly_net_deposit * current_tax_const[1],
                                                                                                                pension_monthly_net_deposit * current_tax_const[2],
                                                                                                                monthly_deposit)
        )
        st.write(
            """You expect to be a :green[{}] tax payer in retirement, so will pay :red[{:,.0f}%] tax. 
            You do not pay national insurance on pension drawdown""".format(retirement_tax_const[0],
                                                                        retirement_tax_const[1] * 100)
        )
        st.write(
            """To take home :green[£{:,.2f}] net from you pension, you would need to withdraw :green[£{:,.2f}]""".format(retirement_monthly_withdrawal, 
                                                                                                            pension_monthly_net_withdrawal)
        )
        st.write(
            """(Of your :green[£{:,.2f}] withdrawal, 25% (:green[£{:,.2f}]) can be taken tax free, and 
            the remaining 75% (:green[£{:,.2f}]) is taxed as income (:red[£{:,.2f}] taken as tax leaving :green[£{:,.2f}] after tax). 
            This totals :green[£{:,.2f}] net take home)""".format(pension_monthly_net_withdrawal,
                                                            pension_monthly_net_withdrawal * 0.25,
                                                            pension_monthly_net_withdrawal * 0.75,
                                                            pension_monthly_net_withdrawal * 0.75 * retirement_tax_const[1],
                                                            pension_monthly_net_withdrawal * 0.75 * (1 - retirement_tax_const[1]),
                                                            retirement_monthly_withdrawal)
        )


    if salary_sacrifice == 'Yes':
        st.write("""Showing results for a :green[salary sacrifice] pension""")
        detailedexplanationss()
    else:
        st.write("""Showing results for :green[SIPP] deposits""")
        detailedexplanationsipp()



    pension_accumulation_df = accumulation_df[['Month','Net take home','Pension deposit','Pension fund','Growth']].copy()

    pension_accumulation_df['Tax relief'] = pension_monthly_net_deposit * current_tax_const[1]

    pension_accumulation_df['NI relief'] = pension_monthly_net_deposit * current_tax_const[2]

    pension_drawdown_df = drawdown_df[['Month','Net take home','Pension deposit','Pension fund','Growth']].copy()

    pension_drawdown_df['Tax relief'] = -pension_monthly_net_withdrawal * 0.75 * retirement_tax_const[1]

    pension_drawdown_df['NI relief'] = 0

    pension_schedule_df = pd.concat([pension_accumulation_df,pension_drawdown_df])

    pension_schedule_df['Pension fund month returns'] = pension_schedule_df['Growth'] / 100 / 12 * pension_schedule_df['Pension fund']



    with st.expander('Show accumulation/drawdown schedule'):
        show_pension_growth = st.toggle(
            'Show monthly pension fund investment returns?',
            help='''Will show the expected returns for a given month based on the size of the fund and
                the expected rate(s) of return. This could be helpful for determining whether the fund is 
                self sustaining (as desired when following the "4% rule" for example)'''
        )



        pension_columns_to_show = ['Month','Net take home','Tax relief','Pension deposit','Pension fund']

        if salary_sacrifice == 'Yes':
            pension_columns_to_show.insert(3, 'NI relief')

        if show_pension_growth:
            pension_columns_to_show.append('Pension fund month returns')


        st.dataframe(pension_schedule_df[pension_columns_to_show].style.format('£{:,.2f}',pension_columns_to_show[1:]),
                    hide_index=True,
                    column_config={
                        'Tax relief': st.column_config.NumberColumn(help='''Will appear as a positive number in accumulation (indicating relief), and a negative number in drawdown 
                                                                        (indicating tax paid)''')
                    })
        
    with st.expander('Show graph'):
        st.line_chart(pension_schedule_df,x='Month',y='Pension fund')



with tab3:



    st.write(
        'LISAs pays a :green[25%] bonus on any deposits'
    )

    st.write(
        '''Giving up :green[£{:,.2f}] of your net income would result in :green[£{:,.2f}] being deposited into your LISA'''.format(monthly_deposit,lisa_monthly_deposit)
    )

    st.write(
        'No tax is paid on LISA withdrawals'
    )

    st.write(
        '''To take home :green[£{0:,.2f}] net from your LISA, you would need to withdraw :green[£{0:,.2f}]'''.format(retirement_monthly_withdrawal)
    )


    with st.expander('Show accumulation/drawdown schedule'):


        show_lisa_growth = st.toggle(
            'Show monthly LISA fund investment returns?',
            help='''Will show the expected returns for a given month based on the size of the fund and
                    the expected rate(s) of return. This could be helpful for determining whether the fund is 
                    self sustaining (as desired when following the "4% rule" for example)'''
        )

        accumulation_df['LISA bonus'] = accumulation_df['Net take home'] * -0.25
        drawdown_df['LISA bonus'] = 0
        lisa_schedule_df_columns = ['Month','Net take home','LISA bonus','LISA deposit','LISA fund','Growth']
        lisa_schedule_df = pd.concat([accumulation_df[lisa_schedule_df_columns],drawdown_df[lisa_schedule_df_columns]])

        if show_lisa_growth:
            lisa_schedule_df['LISA fund month returns'] = lisa_schedule_df['Growth'] / 100 / 12 * lisa_schedule_df['LISA fund']
            lisa_schedule_df_columns.remove('Growth')
            lisa_schedule_df_columns.append('LISA fund month returns')
            lisa_schedule_df.drop(columns=['Growth'],inplace=True)

            st.dataframe(lisa_schedule_df.style.format('£{:,.2f}',lisa_schedule_df_columns[1:]),
                    hide_index=True)
        else:
            lisa_schedule_df_columns.remove('Growth')
            lisa_schedule_df.drop(columns=['Growth'],inplace=True)
            st.dataframe(lisa_schedule_df.style.format('£{:,.2f}',lisa_schedule_df_columns[1:]),
                    hide_index=True)    


    with st.expander('Show graph'):
        st.line_chart(lisa_schedule_df,x='Month',y='LISA fund')


    st.warning(
        '''The age limits on depositing and withdrawing from LISAs adds some complexity when 
        attempting to compare regular contributions to a pension or an ISA 
        \nThis is a complicated idea to articulate, and it does not take away from the general results already shown (i.e. what 
        the relative returns are for one retirement vehicle compared to another), but does influence the accuracy of some of the 
        specific figures shown
        \nTo see a detailed explanation of this, as well as alternative visual comparisons, toggle the below button'''
    )

    show_detailed_lisa = st.toggle(
        'Show LISA deposit/withdrawal age limitation impacts'
    )

    if show_detailed_lisa:
        st.write(
            '''The current age restriction for **withdrawing** from a LISA (without penalty) is **60**. The current 
            age restriction for **depositing** into a LISA is age **50**. This means there is **at minimum 10 
            years** before your desired retirement date where you will not be able to deposit any more funds to a LISA'''
        )

        st.write(
            '''For example, with a time until retirement of :green[30] years, you would only be able to 
            contribute to a LISA for at most :green[20] years'''
        )

        st.write(
            '''This makes comparisons to the lifetime accumulation/drawdown of a pension or ISA difficult, because you are free to deposit to those accounts 
            up until retirement and beyond. This could obfuscate the benefits of a LISA when those deposits are available 
            \nIt would not be fair to show the lifetime accumulation/drawdown of a pension or ISA with 10 extra years of monthly deposits, however 
            it may be of interest to you to have the above "Retirement withdrawal" figures revised for if 
            deposits to **all** accounts stopped 10 years before your desired retirement age 
            \nThis will demonstrate that the *relative* benefits of each account are consistent, and will provide more accurate comparable figures'''
        )

        st.divider()


        if retirement_age <= 10:
            st.write(
                '''As you selected a time until retirement of :green[{}] years, it is not possible to show you the impact this would 
                have on your retirement funds, as you would not be able to make any contributions'''.format(retirement_age)
            )
        else:
            st.write('''With :green[{}] years until retirement, you would be able to contribute to a LISA for 
                    at most :green[{}] years'''.format(retirement_age,retirement_age-10))
            st.write('''in :green[{}] years you could have accumulated:'''.format(retirement_age-10))
        
            retirement_fvs_10_years_less = -npf.fv(
                growth_rate / 100 / 12,
                (retirement_age - 10) * 12,
                [pension_monthly_net_deposit,lisa_monthly_deposit,monthly_deposit],
                0
            )

            for idx,i in enumerate(retirement_fvs_10_years_less):
                st.write("\n* :green[£{:,.2f}] in your {}".format(i,retirement_vehicles[idx]))

            st.write('''After a further :green[10] years of growth (with no additional deposits), you could have accumulated:''')

            retirement_fvs_10_years_less_at_age = -npf.fv(
                growth_rate / 100 / 12,
                10 * 12,
                0,
                retirement_fvs_10_years_less
            )


            for idx,i in enumerate(retirement_fvs_10_years_less_at_age):
                st.write("\n* :green[£{:,.2f}] in your {}".format(i,retirement_vehicles[idx]))


            st.write(
            """In order to receive :green[£{:,.2f}] net per month in retirement from these funds, you would need to withdraw:""".format(retirement_monthly_withdrawal))
            st.write("""\n* :green[£{:,.2f}] a month from your pension""".format(pension_monthly_net_withdrawal))

            st.write("""\n* :green[£{:,.2f}] a month from your LISA""".format(retirement_monthly_withdrawal))

            st.write("""\n* :green[£{:,.2f}] a month from your ISA""".format(retirement_monthly_withdrawal))


            retirement_withdrawal_durations_10_years_less = abs(npf.nper(
            retirement_growth_rate / 100 / 12,
            [-pension_monthly_net_withdrawal,-retirement_monthly_withdrawal,-retirement_monthly_withdrawal],
            retirement_fvs_10_years_less_at_age
            ))

            st.write("This means you could receive :green[£{:,.2f}] net a month (assuming your fund grows at :green[{:,.2f}%]) for:".format(retirement_monthly_withdrawal,retirement_growth_rate))


            for idx, i in enumerate(retirement_withdrawal_durations_10_years_less):
                if np.isnan(i):
                    st.write("\n* :green[Forever] from your {}".format(retirement_vehicles[idx]))
                else:
                    st.write("\n* :green[{:.0f} years] and :green[{:.0f} months] from your {}".format(i / 12,i / 12 % 1 * 12, retirement_vehicles[idx]))

                    
            retirement_withdrawal_pmt_10_years_less = -npf.pmt(
                retirement_growth_rate / 100 / 12,
                retirement_duration * 12,
                retirement_fvs_10_years_less_at_age
            )



            retirement_withdrawal_pmt_10_years_less[0] = retirement_withdrawal_pmt_10_years_less[0] * 0.25 + retirement_withdrawal_pmt_10_years_less[0] * 0.75 * ((1 - brt_tax_rate) if retirement_tax == 'BRT' else (1-hrt_tax_rate))


            st.write("Alternatively, by withdrawing consistently for exactly :green[{:.0f} years] you could be receiving:".format(retirement_duration))

            for idx, i in enumerate(retirement_withdrawal_pmt_10_years_less):
                st.write("\n* :green[£{:,.2f}] a month from your {}".format(i, retirement_vehicles[idx]))


            accumulation_10_years_less_df = accumulation_df.loc[:retirement_age*12-121,['Month','Growth','Net take home','Pension deposit','LISA deposit','ISA deposit','Pension fund','LISA fund','ISA fund']].copy()



            accumulation_10_years_growth_df = pd.DataFrame({
                'Month': np.arange(120) + (retirement_age * 12) - 119,
                'Growth': growth_rate,
                'Net take home': 0,
                'Pension deposit': 0,
                'LISA deposit': 0,
                'ISA deposit': 0
            })



            accumulation_10_years_growth_df['Pension fund'] = -npf.fv(
                growth_rate / 100 / 12,
                accumulation_10_years_growth_df['Month'] - (retirement_age * 12 - 120),
                0,
                retirement_fvs_10_years_less[0]
            )

            accumulation_10_years_growth_df['LISA fund'] = -npf.fv(
                growth_rate / 100 / 12,
                accumulation_10_years_growth_df['Month'] - (retirement_age * 12 - 120),
                0,
                retirement_fvs_10_years_less[1]
            )

            accumulation_10_years_growth_df['ISA fund'] = -npf.fv(
                growth_rate / 100 / 12,
                accumulation_10_years_growth_df['Month'] - (retirement_age * 12 - 120),
                0,
                retirement_fvs_10_years_less[2]
            )


            drawdown_10_years_less_df = pd.DataFrame(
                {
                    'Month': drawdown_months + retirement_age * 12,
                    'Growth': retirement_growth_rate,
                    'Net take home': retirement_monthly_withdrawal,
                    'Pension deposit': -pension_monthly_net_withdrawal,
                    'LISA deposit': -retirement_monthly_withdrawal,
                    'ISA deposit': -retirement_monthly_withdrawal
                }
            )

            drawdown_10_years_less_df['Pension fund'] = -npf.fv(
                retirement_growth_rate / 100 / 12,
                drawdown_10_years_less_df['Month'] - retirement_age * 12,
                drawdown_10_years_less_df['Pension deposit'],
                retirement_fvs_10_years_less_at_age[0]
            )


            drawdown_10_years_less_df['LISA fund'] = -npf.fv(
                retirement_growth_rate / 100 / 12,
                drawdown_10_years_less_df['Month'] - retirement_age * 12,
                drawdown_10_years_less_df['LISA deposit'],
                retirement_fvs_10_years_less_at_age[1]
            )

            drawdown_10_years_less_df['ISA fund'] = -npf.fv(
                retirement_growth_rate / 100 / 12,
                drawdown_10_years_less_df['Month'] - retirement_age * 12,
                drawdown_10_years_less_df['ISA deposit'],
                retirement_fvs_10_years_less_at_age[2]
            )

            schedule_10_years_less_df = pd.concat([accumulation_10_years_less_df,accumulation_10_years_growth_df,drawdown_10_years_less_df])

            schedule_10_years_less_df['Pension fund month returns'] = schedule_10_years_less_df['Growth'] / 100 / 12 * schedule_10_years_less_df['Pension fund']
            schedule_10_years_less_df['LISA fund month returns'] = schedule_10_years_less_df['Growth'] / 100 / 12 * schedule_10_years_less_df['LISA fund']
            schedule_10_years_less_df['ISA fund month returns'] = schedule_10_years_less_df['Growth'] / 100 / 12 * schedule_10_years_less_df['ISA fund']


            with st.expander('Show table'):
                show_lisa_10_years_less_growth = st.toggle(
                    'Show monthly LISA fund investment returns?',
                    help='''Will show the expected returns for a given month based on the size of the fund and
                        the expected rate(s) of return. This could be helpful for determining whether the fund is 
                        self sustaining (as desired when following the "4% rule" for example)''',
                    key='Show adjusted LISA growth toggle'
                )


                lisa_10_years_less_columns = ['Month','Net take home','Pension deposit','LISA deposit','ISA deposit','Pension fund','LISA fund','ISA fund']

                if show_lisa_10_years_less_growth:
                    lisa_10_years_less_columns.extend(['Pension fund month returns','LISA fund month returns','ISA fund month returns'])

                lisa_10_years_less_columns_help = {}

                for i in lisa_10_years_less_columns:
                    if i == 'Month':
                        pass
                    elif i == 'Net take home':
                        lisa_10_years_less_columns_help[i] = st.column_config.NumberColumn(help="""Amount taken/received net to you per month (will be negative when 
                                                                    saving for retirement and positive when withdrawing)""")
                    elif "deposit" in i:
                        lisa_10_years_less_columns_help[i] = st.column_config.NumberColumn(help="""Amount which will be deposited/withdrawn from the fund by month""")
                    elif "fund" in i:
                        lisa_10_years_less_columns_help[i] = st.column_config.NumberColumn(help="""Total value of the fund by month (including growth)""")
                    else:
                        lisa_10_years_less_columns_help[i] = st.column_config.NumberColumn(help="""How much the fund generated each month based on it's value and the expected rate of return""")

                    
                st.dataframe(
                    schedule_10_years_less_df[lisa_10_years_less_columns].set_index('Month').style.format('£{:,.2f}'),
                    column_config=lisa_10_years_less_columns_help
                )




            with st.expander('Show graph'):
                st.line_chart(schedule_10_years_less_df,x='Month',y=['Pension fund','LISA fund','ISA fund'])



with tab4:

    st.write(
        """Giving up :green[£{:,.2f}] of your net income would result in :green[£{:,.2f}] being 
        deposited into your pension""".format(monthly_deposit,monthly_deposit)
    )

    st.write(
        """No tax is paid on ISA withdrawals"""
    )

    st.write(
        """To take home :green[£{:,.2f}] net from your ISA, you would need to withdraw :green[£{:,.2f}]""".format(retirement_monthly_withdrawal,retirement_monthly_withdrawal)
    )

    with st.expander('Show table'):

        show_isa_growth = st.toggle(
            'Show monthly ISA fund investment returns?',
            help='''Will show the expected returns for a given month based on the size of the fund and
                the expected rate(s) of return. This could be helpful for determining whether the fund is 
                self sustaining (as desired when following the "4% rule" for example)''',
            key='Show ISA growth toggle'
        )

        isa_columns = ['Month','Net take home','ISA deposit','ISA fund']

        isa_schedule_df = pd.concat([accumulation_df,drawdown_df])

        isa_schedule_columns = ['Month','Net take home','ISA deposit','ISA fund']

        if show_isa_growth:
            isa_schedule_df['ISA fund month returns'] = isa_schedule_df['Growth'] / 100 / 12 * isa_schedule_df['ISA fund']
            isa_schedule_columns.append('ISA fund month returns')
        
        
        st.dataframe(isa_schedule_df[isa_schedule_columns].set_index('Month').style.format('£{:,.2f}'))

    with st.expander('Show graph'):
        st.line_chart(isa_schedule_df,x='Month',y=['ISA fund'])
