# -- coding: utf-8 --
from __future__ import division
import os

def find_beginning_of_posts(text):
    flag1 = False
    idx = 0

    for line in text:
        if line.startswith("Highlights"):
            flag1 = True
        if flag1 and "News Feed" in line:
            idx += 2
            break
        idx += 1
    return idx

def find_end_of_posts(text, start):
    idx = 0
    for line in text[start:]:
        if line.startswith(" 1."):
            break
        idx += 1
    return start + idx

def find_end_of_next_post(text, beginning):
    idx = 0
    for line in text[beginning+1:]:
        if line.startswith("    <#>"):
            break
        idx += 1
    return beginning + idx + 1

def extract_posts(text):
    start = find_beginning_of_posts(text)
    finish = find_end_of_posts(text, start)
    it = 0
    posts = []

    start_post = start
    end_post = find_end_of_next_post(text, start_post)
    post = text[start_post:end_post+1]
    posts.append("\n".join(post))

    last_end_post = end_post # sanity check
    while True:
        it += 1
        start_post = end_post
        end_post = find_end_of_next_post(text, start_post)

        # check that we don't stuck
        if last_end_post == end_post:
            break
        else:
            last_end_post = end_post
        # check until we reach finish line
        if end_post < finish:
            post = text[start_post:end_post+1]
            posts.append("\n".join(post))
        else:
            post = text[start_post:finish]
            posts.append("\n".join(post))
            break
    return posts

# TODO parse each post: date, content, author, likes

def get_likes(snippet):
    number_of_likes = 0
    previous_line = ""
    for line in snippet:
        # TODO add handling you case
        # if "You" or "you" in line:
        #     print line
        #     number_of_likes += 1
        if "<http" in line:
            number_of_likes += 1
        if "people" in line or "others" in line:
            splitted = line.split()
            for idx, word in enumerate(splitted):
                if (word == "people" or word == "others"):
                    if idx != 0:
                        number_of_likes += int(splitted[idx - 1])
                    else:
                        number_of_likes += int(previous_line.split()[-1])
                    break
        previous_line = line
    return number_of_likes

def get_like_snippet(post):
    post = post.split("\n")
    second = False
    likes_snippet_start = False
    for idx, line in enumerate(post):
        if "ike <#> ·" in line:
            start_likes = idx
            likes_snippet_start = True
        elif "*" in line and likes_snippet_start:
            if not second:
                second = True
            else:
                end_likes = idx
                # print start_likes, end_likes
                break
    else:
        end_likes = idx
        # print start_likes, end_likes
    like_snippet = post[start_likes:end_likes]
    return like_snippet


if __name__ == "__main__":

    with open("dump_folder/my_friends_walls/Roman Prilepskiy.html") as f:
        # text = [line for line in f]
        text = []
        for line in f:
            text.append(line.split(os.linesep)[0])
    # for i, line in enumerate(text):
    #     print i, line[:20]
    start= find_beginning_of_posts(text)
    finish = find_end_of_posts(text, start)
    end = find_end_of_next_post(text, start)
    # print start
    # print finish
    # print end
    # print text[finish]
    # print '\n'.join(text[start:end])
    posts = extract_posts(text)
    for idx, post in enumerate(posts):
        print post
        snippet = get_like_snippet(post)
        print "Post %s has %s likes" %(idx + 1, get_likes(snippet))
        print '*************************'
        print
    # snippet = get_like_snippet(post)
    # print get_likes(snippet)

    console = []