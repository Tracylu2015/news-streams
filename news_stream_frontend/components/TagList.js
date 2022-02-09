import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { View, FlatList, StyleSheet, Text, Image, RefreshControl, Pressable, Linking } from "react-native";



const TagList = ({ tag }) => {

    const [tweet, setTweet] = useState([])
    const baseUrl = 'https://news-stream.spookyai.com';
    const [refresh, setRefresh] = useState(false)
    const [onPull, setOnPull] = useState(false)

    useEffect(() => {
        const source = axios.CancelToken.source();
        const url = `${baseUrl}/api/tags/${tag}`;
        const fetchTrends = async () => {
            try {
                setRefresh(true)
                const response = await axios.get(url, { cancelToken: source.token });
                setTweet([...response.data])

            } catch (error) {
                if (axios.isCancel(error)) {
                    console.log('Data fetching cancelled');
                }
            }
            finally {
                setRefresh(false)
            }
        };
        fetchTrends();
        return () => source.cancel("Data fetching cancelled");
    }, [tag, onPull]);

    const Item = ({ item }) => (
        <View style={styles.item}>
            <Text style={styles.title}>{item}</Text>
        </View>
    );

    const ProfileItem = ({ item }) => (
        <View style={styles.item}>
            <Text style={styles.screenName}>{item}</Text>
        </View>
    );

    const Location = ({ item }) => (
        <View style={styles.item}>
            <Text style={{ fontSize: 12, color: '#4a99e9' }}>{item}</Text>
        </View>
    );

    const Time = (item) => {
        var now = new Date().getTime()
        var post_time = parseInt(item.created_at["$date"])
        var diff = Math.floor((now - post_time) / 1000)
        if (0 <= diff && diff < 60) {
            console.log(now, post_time, diff)
            return "posted just now";
        } else if (60 < diff && diff < 3600) {
            return "posted " + Math.floor(diff / 60) + " mins ago";
        } else if (3600 <= diff && diff < 86400) {
            return "posted " + Math.floor(diff / 3660) + " hours ago";
        } else {
            post_time = new Date(item.created_at["$date"]).toDateString()
            return post_time;
        }
    }


    const info = (item) => {
        let username = item.user_info.screen_name
        let UserProfileURL = `https://twitter.com/${username}`
        Linking.openURL(UserProfileURL)
    }

    const toOriginal = (item) => {
        let postId = item.post_id
        let OriginalURL = `https://twitter.com/i/web/status/${postId}`
        Linking.openURL(OriginalURL)
    }


    const renderItem = ({ item }) => (
        <View style={[styles.item, styles.elevation]}>
            <Pressable onPress={() => info(item)}>
                <View style={styles.profile}>
                    <Image style={styles.tinyLogo} source={{ uri: item.user_info.profile_image_url }} />
                    <View>
                        <ProfileItem item={item.user_info.screen_name} />
                    </View>
                    <View>
                        {item.user_info.verified === true ? <Image style={styles.icon} source={require("./images/verified.png")} /> : null}
                    </View>
                </View>
            </Pressable>
            <Pressable onPress={() => toOriginal(item)}>
                <View >
                    {item.user_info.hasOwnProperty("location")
                        ?
                        <View style={styles.row}>
                            <Image style={styles.pin} source={require("./images/pin.png")} />
                            <Location item={item.user_info.location} />
                        </View>
                        : null}
                </View>
                <View>
                    <Item item={item.text} />
                </View>
                <View>
                    {item.hasOwnProperty("media_url") 
                    ? <Image style={styles.tImage} source={{ uri: item.media_url }} /> 
                    : null}
                </View>
                <View>
                    <Text style={styles.text}>{Time(item)}</Text>
                </View>
                <View style={styles.row} >
                    <View style={styles.row}>
                        <Item item={item.user_info.followers_count} />
                        <Text style={styles.text}>
                            followers
                        </Text>
                    </View >
                    <View style={styles.row}>
                        <Item item={item.user_info.friends_count} />
                        <Text style={styles.text}>
                            friends
                        </Text>
                    </View>
                </View>
            </Pressable >
        </View>
    );

    return (

        <FlatList
            refreshControl={
                <RefreshControl
                    refreshing={refresh}
                    onRefresh={() => setOnPull(true)}
                    colors={['#4a99e9']}
                />}
            data={tweet}
            renderItem={renderItem}
            keyExtractor={(item, index) => index}
            onPress={() => Linking.openURL(UserProfileURL)}
        />
    );
};

const styles = StyleSheet.create({
    item: {
        backgroundColor: '#dedede',
        padding: 4,
        marginVertical: 10,
        marginHorizontal: 10,
        borderRadius: 8,
    },
    elevation: {
        elevation: 15,
        shadowColor: '#000022',
    },
    title: {
        fontSize: 16,
        color: '#000022'
    },
    row: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
    },
    text: {
        fontSize: 16,
        color: '#000022',
        marginLeft: 15,
        marginTop: 5,
    },
    tinyLogo: {
        width: 50,
        height: 50,
        borderRadius: 25,
    },
    profile: {
        flex: 1,
        flexDirection: 'row',
        marginLeft: 16,
        paddingTop: 20,
        alignItems: 'center'
    },
    screenName: {
        fontWeight: 'bold',
        fontSize: 24,
        color: '#000022',
    },
    icon: {
        width: 20,
        height: 20,
        top: 2,
    },
    tImage: {
        width: 360,
        height: 200,
        marginLeft: 12,
    },
    pin: {
        width: 20,
        height: 20,
        marginLeft: 16,
    },
})

export default TagList;
