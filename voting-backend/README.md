# Voting Backend

The voting backend should be easy - fix line 26 to point to the correct topic and create a new lambda function using the provided sample.

In order for a function to post to a topic, it must have the appropriate policy attached to the role. More granular iam policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:us-east-1:025416187662:erjan"
        }
    ]
}
```

The above example will work, but it has a drawback: in this case, the function can publish messages to any topic, and this is redundant. Try setting the policy so that messages can only be sent to one topic.
