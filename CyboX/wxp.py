# -*- coding: utf-8 -*-

import wx
import report

if __name__ == "__main__":
  report.mininginfo()
  application = wx.App()

  frame = wx.Frame(None, wx.ID_ANY, u"CybOX Document Creater")
  #ステータスバーの利用
  frame.CreateStatusBar()
  frame.SetStatusText("LIFT-S.com")


  panel = wx.Panel(frame,wx.ID_ANY)
  button_1 = wx.Button(panel, wx.ID_ANY,"CybOX")

  s_text_1 = wx.StaticText(panel,wx.ID_ANY,report.sys_info)

  layout = wx.BoxSizer(wx.HORIZONTAL)
  layout.Add(button_1)
  layout.Add(s_text_1)
  panel.SetSizer(layout)

  frame.Show()
  application.MainLoop()
