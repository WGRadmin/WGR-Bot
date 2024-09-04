const { Client, GatewayIntentBits, Partials, ActionRowBuilder, ButtonBuilder, ButtonStyle, EmbedBuilder, Events, REST, Routes } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ],
    partials: [Partials.Channel],
});

const token = 'botのトークン';
const channelId = '認証完了通知用チャンネル';
const roleName = '付与するロール';

client.once('ready', () => {
    console.log('botの準備完了！');
    client.user.setActivity('/create', { type: 'WATCHING' });
});

client.on(Events.InteractionCreate, async (interaction) => {
    if (interaction.isCommand()) {
        const { commandName } = interaction;

        if (commandName === 'create') {
            const row = new ActionRowBuilder()
                .addComponents(
                    new ButtonBuilder()
                        .setCustomId('accept')
                        .setLabel('はい')
                        .setStyle(ButtonStyle.Primary),
                    new ButtonBuilder()
                        .setCustomId('decline')
                        .setLabel('いいえ')
                        .setStyle(ButtonStyle.Danger)
                );

            const embed = new EmbedBuilder()
                .setTitle('規約本文')
                .setDescription('規約に同意しますか？')
                .setColor('#ffffff');

            await interaction.reply({ embeds: [embed], components: [row] });
        }
    } else if (interaction.isButton()) {
        if (interaction.customId === 'accept') {
            await interaction.deferReply({ ephemeral: true });

            const member = interaction.guild.members.cache.get(interaction.user.id);
            if (member) {
                const role = member.roles.cache.find((r) => r.id === roleName);
                if (!role) {
                    await member.roles.add(roleName);
                }
            }

            const successEmbed = new EmbedBuilder()
                .setTitle('認証成功')
                .setDescription(`${interaction.user}さんの認証に成功しました！`)
                .setColor('#00ff00');
            await interaction.followUp({ embeds: [successEmbed], ephemeral: true });

            const channelToSend = interaction.guild.channels.cache.get(channelId);
            if (channelToSend) {
                const successMessageEmbed = new EmbedBuilder()
                    .setTitle('認証成功')
                    .setDescription(`${interaction.user}さんが認証に成功しました！`)
                    .setColor('#00ff00');
                await channelToSend.send({ embeds: [successMessageEmbed] });
            }
        } else if (interaction.customId === 'decline') {
            await interaction.reply({ content: '規約に同意されませんでした。', ephemeral: true });
        }
    }
});

client.login(token);
