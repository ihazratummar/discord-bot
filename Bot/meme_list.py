import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import discord

RANDOM_MEME_LIST = [
    "https://cdn.discordapp.com/attachments/874162166343815229/1103965676512755792/meme.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005488854704210/8000_a_month_minimum_3e2c987aed103bbb84509945fa93d96c.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005506621775912/A_lesson_that_took_me_some_time_to_learn_c44d90161370ed8a01e64dfae599b3a0.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005511755616337/Absolute_Chaos_b1c5b969c782867a0c4e76dc20727827.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005516709085194/And_do_enjoy_your_vacations_74e4e8ec1e086acbacc92716bdb75d1f.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005543078678558/Anyone_else_getting_tired_of_this_a41695610bf7fe80561d7e09c8bf38eb.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005547549790248/As_a_living_breathing_human_being_I_am_quite_afraid_of_the_implications._837485f75557237a36b1ea0205872aa2.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005554973724743/Baby_Yoda__Minion_09dcdd12e632ebc26846575b33fd2273.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005559138660384/at_least_chili_doesnt_contaminate_everything_8bb02a629c456504a73e5164e274d47c.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005562347294801/Bad_skin_day._34959a629524cf4b69d3c7a617a31a34.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005571356655656/Bigger_is_better_d9b082ca93599521987567f8a658cae4.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005579200012358/cant_let_that_free_food_slide_3370022cff4b5171d9aa21d26f70e133.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005588347785286/Chew_on_that_for_a_while_9fc8d687a8cbecebaf655d2cdf583aeb.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005599282352238/Consider_the_squad_fucked_dc2a94adb86f329005c51fef240ee3cc.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005605036929074/Depression_gone_in_an_instant_a5c977f10193f821205d496c67338e5d.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005608077803621/Deep_rock_galactic_did_it_right_f642e630580a02b67ebc986a2d710441.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005611437424720/Diesel_paid_too_much_fad6064f2720a2b0fbe356634509f811.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005614222454805/Different_Day_SMe_Situation_11e55cbf04bde73cf8df8c8fdf6750f2.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005625010204692/Difficult_times_make_difficult_choices_03c2c0fe5f6ef2fdc919d722810f95d8.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005627967197194/Diggy_diggy_indeed..._ee6042b5267290076e73de318bf438f2.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005635395293246/Educational_meme._db144d673f68511666613b179071c646.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005650792591371/Every_DC_movie_9079989dd0ca501327b848c554724fd9.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005662842834955/Every_little_bit_counts_you_know_2e7bcc08b17b83f2b4c4df82adc7cb85.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005783101919284/Fucking_pollen_d194f5eb2516ad889417f689d9fb1b32.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005786109218876/FR_tho._fdcbda6f3a6db0d89fa69d2190c5a3cb.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005790265782292/Good_news__e2a2417c214e39f8cad27cede21edde6.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005801548460082/Gotta_love_bank_closures_a84f6cc7d7286a5d4b53d610868b59f4.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005809127555193/Hes_not_okay_I_promise_b1734044c85d2e75059a56d47a5b6b8e.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005812675944548/Guess_again_32e4f5ac49a153517551d2fe79792fb0.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005815532261427/Hes_not_The_original_rebel._I_Am_eb05222181c5f425a6e93b95049d07bf.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005818535378944/He_wasnt_ready_to_die_that_day_682c12b7d85c8e8257bd4cc6940b0728.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005821169410068/I_cant_be_alone_with_this_right_83ab4fc5d8836e99c79a87993b559f5b.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005823912476744/i_did_not_see_that_coming_617535504409a2cdcbadd6fddaa27a1c.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005826882052208/I_dont_think_thats_what_he_meant_4a86c307c33389a9fa8a80346650ad95.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005833928482896/I_hate_that_couch_co-op_video_games_are_almost_non-existant_nowadays_058fb7324330c033eef4e2b111b6f552.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005841809588274/I_like_the_word_Drahtesel__554182364c7583cfc2ca56f6c40026e6.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005850902835221/I_made_an_oopsie_26670132c13e45d7d53cec6420e2d599.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005854467989615/I_support_the_WGA_strike._92c5f6bc742ecfc98527136152e5d218.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005863246680074/I_want_a_relationship_but_feel_trapped_when_I_get_one._f077b47fccf79f8fc3ee2db1f8997901.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005873275256892/IM_the_captain_now_b536bdbe1af6b481a3bbf77b173847c7.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005876701999124/Im_to_dumb_to_understand_26b68da9aa218de383d0ba3c277704a1.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005884373368832/It_hits_different_1e4d7937061e9704ee1633c1c75f27d2.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005886835445780/It_is_kind_of_suspicious_dont_you_think_270f4e77a672abd52ca85e45cadbba2e.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005891558215781/It_is_what_it_is_ae4147ad4407f782042057c3126be8c5.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005905571385416/Its_all_gonna_touch_eventually_1d7f6c44fdb707720f2c82dc0b55e80a.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005914794672149/Its_true_76ff777b418d0419b12da7e96b2f9e53.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005917499998328/judgemental_clouds_0cf5b3fd601eaf5db1539d10313bb3bc.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005925678882947/Jesse_get_me_the_DVD_player_fe6ff38f0cc33650c88c5b73328633d8.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005928900100176/Logo_name_suggestions_4deaaf299e5d9eb1d0f5749d501aa104.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005932129726504/Let_the_chaos_ensue_fd80d9a4efdf786b8d2fd96434ef073e.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005935229309029/Let_us_have_a_detailed_discussion_54525b9f86efd760f792c41da551aad1.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005951285100614/May_fourth_fc57546913cee853e9178c2295b2bdc0.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005971774279701/Next_time_be_more_clear_about_your_present_request_2fb32cb240b19057a40907ede21e8b6d.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005981026918401/Off_to_a_bad_start_e162439749e367269739737b2a52df5d.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005994259955754/Probably_not_what_they_envisioned._cb207e9a9e9884d4e7c96734832096a5.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104005998076756068/Quite_the_look_847c1f727c5434d8f4ad592ed3cc1295.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006004607291412/Remember_who_ur_talking_to_25ecfe3811925c5a002375f75376782f.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006007337787442/relatable_2c332ad0df4b783c59c5e25011fdab2e.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006021720055808/The_electric_boogaloo_145676ef17d68402ebd7792d95ec91ff.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006025968889968/The_fact_he_was_actually_36_makes_it_even_better_6d6f44d93e877beddfeac001ec54b7ef.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006032595894393/THE_hallway_e544d3f9781c701bde862cdb29dd7abb.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006045946368030/The_horror_168053b139a0633e089c0bd2231c43d5.png",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006056994156555/This_just_a_joke_6369d1e5b79ce951d97775119f9302bc.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006062081839134/Theyve_cured_disease_stopped_crime_and_solved_poverty_a83711fc37df489596ab5f0a31cfd0b7.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006065135304714/Time_is_running_faee71615ffafefca06f2666d6b7e335.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006067622522890/Tots_and_Pears_everyone_a343713edfeeb9a7c814fa8782e422ad.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006082092879922/try_not_to_be_creepy_challenge_level_god_required_rank_500_fe33ed8d8890c810cab6df002dea2d72.gif",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006084525555722/When_you_accidentally_say_the_inside_words_out_loud_dddc1ec59d7cb24fae702185965ec623.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006093081944114/WHERE_ARE_THE_GAAAAAAMES_d0fc21eeb38e8ed73546446ea8f6b139.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006099578912819/which_side_are_you_on_f85d5dd3e3b8951c0d881520a1f7ccf3.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006108303077527/Why_is_she_like_this_2154dacd38db929f024768ed8dad86e9.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006129681432687/woof_woof_I_love_you_bestie._91205b6e313e7baa0436f443c85b1740.jpeg",
    "https://cdn.discordapp.com/attachments/1104003925369176124/1104006139328340008/Yes_it_is_coming_in_some_countries_on_the_App_Store_it_has_already_come_out_f00a13583537782ab3e1353b49cee822.png",
]

meme_url = random.choice(RANDOM_MEME_LIST)

print(meme_url)

# for i in RANDOM_MEME_LIST:
#     responses = requests.get(meme_url)
#     image = Image.open(BytesIO(responses.content))

#     caption = "Meme"
#     draw = ImageDraw.Draw(image)
#     font = ImageFont.truetype("Lato-Bold.ttf", 20)
#     draw.text((10, 10), caption, font=font, fill="white")

#     with BytesIO() as image_binary:
#         image.save(image_binary, "PNG")
#         image_binary.seek(0)
#         file = discord.File(fp=image_binary, filename="meme.png")

#     if __name__ == "__main__":
#         RANDOM_MEME_LIST = RANDOM_MEME_LIST
