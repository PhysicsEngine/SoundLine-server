# -*- coding: utf-8 -*-
class VsqxLib(object):
    NOTE_XML = """
<note>
    <posTick>{0}</posTick>
    <durTick>{1}</durTick>
    <noteNum>{2}</noteNum>
        <velocity>64</velocity>
        <lyric><![CDATA[ら]]></lyric>
	<phnms><![CDATA[4 a]]></phnms>
        <noteStyle>
                <attr id="accent">50</attr>
                <attr id="bendDep">8</attr>
                <attr id="bendLen">0</attr>
                <attr id="decay">50</attr>
                <attr id="fallPort">0</attr>
                <attr id="opening">127</attr>
                <attr id="risePort">0</attr>
                <attr id="vibLen">66</attr>
                <attr id="vibType">1</attr>
                <seqAttr id="vibDep">
                        <elem>
                                <posNrm>22391</posNrm>
                                <elv>64</elv>
                        </elem>
                </seqAttr>
                <seqAttr id="vibRate">
                        <elem>
                                <posNrm>22391</posNrm>
                                <elv>50</elv>
                        </elem>
                </seqAttr>
        </noteStyle>
</note>
"""

    VSQX_XML = u"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<vsq3 xmlns="http://www.yamaha.co.jp/vocaloid/schema/vsq3/"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.yamaha.co.jp/vocaloid/schema/vsq3/ vsq3.xsd">
	<vender><![CDATA[Yamaha corporation]]></vender>
	<version><![CDATA[3.0.0.11]]></version>
	<vVoiceTable>
		<vVoice>
			<vBS>0</vBS>
			<vPC>0</vPC>
			<compID><![CDATA[BDRE87E2FTTKTDBA]]></compID>
			<vVoiceName><![CDATA[VY1V3]]></vVoiceName>
			<vVoiceParam>
				<bre>0</bre>
				<bri>0</bri>
				<cle>0</cle>
				<gen>0</gen>
				<ope>0</ope>
			</vVoiceParam>
		</vVoice>
	</vVoiceTable>
	<mixer>
		<masterUnit>
			<outDev>0</outDev>
			<retLevel>0</retLevel>
			<vol>0</vol>
		</masterUnit>
		<vsUnit>
			<vsTrackNo>0</vsTrackNo>
			<inGain>0</inGain>
			<sendLevel>-898</sendLevel>
			<sendEnable>0</sendEnable>
			<mute>0</mute>
			<solo>0</solo>
			<pan>64</pan>
			<vol>0</vol>
		</vsUnit>
		<seUnit>
			<inGain>0</inGain>
			<sendLevel>-898</sendLevel>
			<sendEnable>0</sendEnable>
			<mute>0</mute>
			<solo>0</solo>
			<pan>64</pan>
			<vol>0</vol>
		</seUnit>
		<karaokeUnit>
			<inGain>0</inGain>
			<mute>0</mute>
			<solo>0</solo>
			<vol>-129</vol>
		</karaokeUnit>
	</mixer>
	<masterTrack>
		<seqName><![CDATA[Untitled0]]></seqName>
		<comment><![CDATA[New VSQ File]]></comment>
		<resolution>480</resolution>
		<preMeasure>1</preMeasure>
		<timeSig>
			<posMes>0</posMes>
			<nume>4</nume>
			<denomi>4</denomi>
		</timeSig>
		<tempo>
			<posTick>0</posTick>
			<bpm>12000</bpm>
		</tempo>
	</masterTrack>
	<vsTrack>
		<vsTrackNo>0</vsTrackNo>
		<trackName><![CDATA[Track]]></trackName>
		<comment><![CDATA[Track]]></comment>
		<musicalPart>
			<posTick>1920</posTick>
			<playTime>61440</playTime>
			<partName><![CDATA[NewPart]]></partName>
			<comment><![CDATA[New Musical Part]]></comment>
			<stylePlugin>
				<stylePluginID><![CDATA[ACA9C502-A04B-42b5-B2EB-5CEA36D16FCE]]></stylePluginID>
				<stylePluginName><![CDATA[VOCALOID2 Compatible Style]]></stylePluginName>
				<version><![CDATA[3.0.0.1]]></version>
			</stylePlugin>
			<partStyle>
				<attr id="accent">50</attr>
				<attr id="bendDep">8</attr>
				<attr id="bendLen">0</attr>
				<attr id="decay">50</attr>
				<attr id="fallPort">0</attr>
				<attr id="opening">127</attr>
				<attr id="risePort">0</attr>
			</partStyle>
			<singer>
				<posTick>0</posTick>
				<vBS>0</vBS>
				<vPC>0</vPC>
			</singer>
{0}
		</musicalPart>
	</vsTrack>
	<seTrack>
	</seTrack>
	<karaokeTrack>
	</karaokeTrack>
	<aux>
		<auxID><![CDATA[AUX_VST_HOST_CHUNK_INFO]]></auxID>
		<content><![CDATA[VlNDSwAAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=]]></content>
	</aux>
</vsq3>"""

    @classmethod
    def createNote(cls, posTick, durTick, noteNum):
        xml = unicode(cls.NOTE_XML, 'utf-8')
        return xml.format(posTick, durTick, noteNum)

    @classmethod
    def createVsqx(cls, notes):
        return cls.VSQX_XML.format("\n".join(notes)).encode('utf-8')

notes = [VsqxLib.createNote(1, 2, 3), VsqxLib.createNote(3, 4, 5)]
print VsqxLib.createVsqx(notes)
