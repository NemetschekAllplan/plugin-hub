﻿<?xml version="1.0" encoding="utf-8"?>
<Element xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:noNamespaceSchemaLocation="https://pythonparts.allplan.com/2026/schemas/PythonPart.xsd">
  <Script>
    <Name>PluginManager.py</Name>
    <Title>ALLPLAN Plugin Manager</Title>
    <Version>0.1</Version>
  </Script>
  <Constants>
    <!-- Actions on the overview page of installed plugins (1001-1200) -->
    <Constant>
      <Name>CHECK_ALL_FOR_UPDATES</Name>
      <Value>1002</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>SHOW_DETAILS_INSTALLED_PLUGIN</Name>
      <Value>1003</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <!-- Actions on the overview page of available plugins (1201-1500) -->
    <Constant>
      <Name>SHOW_DETAILS_AVAILABLE_PLUGIN</Name>
      <Value>1201</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>INSTALL_AVAILABLE_PLUGIN</Name>
      <Value>1202</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <!-- Actions on the detail page (1501-2000) -->
    <Constant>
      <Name>EMAIL_TO_SUPPORT</Name>
      <Value>1501</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>GO_TO_GITHUB</Name>
      <Value>1502</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>GO_TO_HOMEPAGE</Name>
      <Value>1503</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>INSTALL</Name>
      <Value>1504</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>CHECK_FOR_UPDATES</Name>
      <Value>1505</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>UPDATE</Name>
      <Value>1506</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>INSTALL_ANOTHER_VERSION</Name>
      <Value>1507</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>EXECUTE_INSTALL_ANOTHER_VERSION</Name>
      <Value>1508</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>UNINSTALL</Name>
      <Value>1509</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <!-- Palette states -->
    <Constant>
      <Name>SHOW_OVERVIEW</Name>
      <Value>2001</Value>
      <ValueType>Integer</ValueType>
    </Constant>
    <Constant>
      <Name>SHOW_DETAILS</Name>
      <Value>2002</Value>
      <ValueType>Integer</ValueType>
    </Constant>
  </Constants>
  <Page>
    <Name>InstalledPlugins</Name>
    <Text>Installed</Text>
    <Visible>CurrentPaletteState == SHOW_OVERVIEW and InstalledPluginNames != ["EMPTY"]</Visible>
    <Parameters>
      <Parameter>
        <Name>CheckForUpdatesROw</Name>
        <Text>Baz</Text>
        <ValueType>Row</ValueType>
        <Value>OVERALL</Value>
        <Parameters>
          <Parameter>
            <Name>Dummy</Name>
            <Text/>
            <Value/>
            <ValueType>Text</ValueType>
            <Orientation>Right</Orientation>
          </Parameter>
          <Parameter>
            <Name>CheckAllForUpdatesButton</Name>
            <Text>Check all for updates</Text>
            <EventId>CHECK_ALL_FOR_UPDATES</EventId>
            <Value>14057</Value>
            <ValueType>PictureResourceButton</ValueType>
            <WidthInRow>5</WidthInRow>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>Separator</Name>
        <ValueType>Separator</ValueType>
      </Parameter>
      <Parameter>
        <Name>InstalledPluginListGroup</Name>
        <ValueType>ListGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>InstalledPluginTitleRow</Name>
            <Text>Foo</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>InstalledPluginNames</Name>
                <Text>Foo</Text>
                <Orientation>Left</Orientation>
                <Value>[_]</Value>
                <ValueType>Text</ValueType>
                <FontFaceCode>1</FontFaceCode>
                <FontStyle>4</FontStyle>
              </Parameter>
              <Parameter>
                <Name>InstalledDetailsButton</Name>
                <Text>Show the plugin details</Text>
                <EventId>SHOW_DETAILS_INSTALLED_PLUGIN</EventId>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>PictureResourceButton</ValueType>
                <WidthInRow>5</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>InstalledPluginDescriptionRow</Name>
            <Text>Bar</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>InstalledPluginDescriptions</Name>
                <Text />
                <Value>[_]</Value>
                <ValueType>Text</ValueType>
                <Visible>InstalledPluginDescriptions[$list_row] != ""</Visible>
                <FontStyle>1</FontStyle>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
            <Visible>$list_row != len(InstalledPluginNames) - 1 </Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>
  <Page>
    <Name>AvailablePlugins</Name>
    <Text>Available</Text>
    <Visible>CurrentPaletteState == SHOW_OVERVIEW and AvailablePluginNames != ["EMPTY"]</Visible>
    <Parameters>
      <Parameter>
        <Name>AvailablePluginListGroup</Name>
        <ValueType>ListGroup</ValueType>
        <Parameters>
          <Parameter>
            <Name>AvailablePluginTitleRow</Name>
            <Text>Foo</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>AvailablePluginNames</Name>
                <Text>Foo</Text>
                <Orientation>Left</Orientation>
                <Value>[_]</Value>
                <ValueType>Text</ValueType>
                <FontFaceCode>1</FontFaceCode>
                <FontStyle>4</FontStyle>
              </Parameter>
              <Parameter>
                <Name>InstallAvailableButton</Name>
                <Text>Download and install</Text>
                <EventId>INSTALL_AVAILABLE_PLUGIN</EventId>
                <Value>8522</Value>
                <ValueType>PictureResourceButton</ValueType>
                <WidthInRow>5</WidthInRow>
              </Parameter>
              <Parameter>
                <Name>AvailableDetailsButton</Name>
                <Text>Show the plugin details</Text>
                <EventId>SHOW_DETAILS_AVAILABLE_PLUGIN</EventId>
                <Value>AllplanSettings.PictResPalette.eHotinfo</Value>
                <ValueType>PictureResourceButton</ValueType>
                <WidthInRow>5</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>AvailablePluginDescriptionRow</Name>
            <Text>Bar</Text>
            <ValueType>Row</ValueType>
            <Value>OVERALL</Value>
            <Parameters>
              <Parameter>
                <Name>AvailablePluginDescriptions</Name>
                <Text />
                <Value>[_]</Value>
                <ValueType>Text</ValueType>
                <Visible>AvailablePluginDescriptions[$list_row] != ""</Visible>
                <FontStyle>1</FontStyle>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <ValueType>Separator</ValueType>
            <Visible>$list_row != len(AvailablePluginNames) - 1 </Visible>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>

  <Page>
    <Name>PluginDetails</Name>
    <Text>Plugin details</Text>
    <Visible>CurrentPaletteState == SHOW_DETAILS</Visible>
    <Parameters>
      <Parameter>
        <Name>PluginExpander</Name>
        <Text>Plugin</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>PluginUUID</Name>
            <Text>UUID</Text>
            <Value/>
            <ValueType>String</ValueType>
            <Visible>False</Visible>
          </Parameter>
          <Parameter>
            <Name>PluginName</Name>
            <Text>Name</Text>
            <Value> </Value>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>InstalledVersion</Name>
            <Text>Installed version</Text>
            <Value> </Value>
            <ValueType>Text</ValueType>
            <Visible>InstalledVersion</Visible>
          </Parameter>
          <Parameter>
            <Name>InstallDate</Name>
            <Text>Installation date</Text>
            <Value> </Value>
            <ValueType>Text</ValueType>
            <Visible>InstallDate</Visible>
          </Parameter>
          <Parameter>
            <Name>InstallLocation</Name>
            <Text>Installed in</Text>
            <Value> </Value>
            <ValueType>Text</ValueType>
            <Visible>InstallLocation</Visible>
          </Parameter>
          <Parameter>
            <Name>PluginGithubRepo</Name>
            <Text>GitHub repository</Text>
            <ValueType>Row</ValueType>
            <Visible>PluginGitHubRepoName</Visible>
            <Parameters>
              <Parameter>
                <Name>PluginGitHubRepoName</Name>
                <Text/>
                <Value></Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>GoToGitHubButton</Name>
                <Text>Go to the plugin repository</Text>
                <EventId>GO_TO_GITHUB</EventId>
                <Value>8631</Value>
                <ValueType>PictureResourceButton</ValueType>
                <WidthInRow>5</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>Separator</Name>
            <Text/>
            <ValueType>Separator</ValueType>
          </Parameter>
          <Parameter>
            <Name>ActionsRow</Name>
            <Text> </Text>
            <ValueType>Row</ValueType>
            <Parameters>
              <Parameter>
                <Name>InstallButton</Name>
                <Text>Download and install</Text>
                <EventId>INSTALL</EventId>
                <Value>8522</Value>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>PluginStatus == 0</Visible>
              </Parameter>
              <Parameter>
                <Name>CheckForUpdatesButton</Name>
                <Text>Check for updates</Text>
                <EventId>CHECK_FOR_UPDATES</EventId>
                <Value>14057</Value>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>PluginStatus == 1 and PluginHasGitHub</Visible>
              </Parameter>
              <Parameter>
                <Name>UpdateButton</Name>
                <Text>Update the plugin</Text>
                <EventId>UPDATE</EventId>
                <Value>8519</Value>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>PluginStatus == 2 and PluginHasGitHub</Visible>
              </Parameter>
              <Parameter>
                <Name>UpToDateButton</Name>
                <Text>Plugin is up to date</Text>
                <EventId>0</EventId>
                <Value>11433</Value>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>PluginStatus == 3 and PluginHasGitHub</Visible>
                <Enable>False</Enable>
              </Parameter>
              <Parameter>
                <Name>InstallAnotherVersionButton</Name>
                <Text>Install another version</Text>
                <EventId>INSTALL_ANOTHER_VERSION</EventId>
                <Value>16975</Value>  <!--11169;14065-->
                <ValueType>PictureResourceButton</ValueType>
                <Visible>PluginStatus != 0 and PluginHasGitHub</Visible>
              </Parameter>
              <Parameter>
                <Name>UninstallButton</Name>
                <Text>Uninstall this plugin</Text>
                <EventId>UNINSTALL</EventId>
                <Value>10051</Value>
                <ValueType>PictureResourceButton</ValueType>
                <Visible>PluginStatus != 0</Visible>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>InstallAnotherVersionRow</Name>
            <Text>Select version </Text>
            <ValueType>Row</ValueType>
            <Visible>False</Visible>
            <Parameters>
              <Parameter>
                <Name>VersionsComboBox</Name>
                <Text>VersionsComboBox</Text>
                <Value/>
                <ValueList/>
                <ValueType>StringComboBox</ValueType>
              </Parameter>
              <Parameter>
                <Name>ExecuteInstallAnotherVersionButton</Name>
                <Text>Install</Text>
                <EventId>EXECUTE_INSTALL_ANOTHER_VERSION</EventId>
                <Value>8522</Value>
                <ValueType>PictureResourceButton</ValueType>
                <Enable>InstalledVersion not in VersionsComboBox</Enable>
                <WidthInRow>10</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
      <Parameter>
        <Name>DeveloperExpander</Name>
        <Text>Developer</Text>
        <Value>False</Value>
        <ValueType>Expander</ValueType>
        <Parameters>
          <Parameter>
            <Name>DeveloperName</Name>
            <Text>Name</Text>
            <Value></Value>
            <ValueType>Text</ValueType>
          </Parameter>
          <Parameter>
            <Name>DeveloperAddress</Name>
            <Text>Address</Text>
            <Value></Value>
            <ValueType>Text</ValueType>
            <Visible>DeveloperAddress</Visible>
          </Parameter>
          <Parameter>
            <Name>DeveloperSupportRow</Name>
            <Text>Support</Text>
            <ValueType>Row</ValueType>
            <Visible>DeveloperSupportEmail</Visible>
            <Parameters>
              <Parameter>
                <Name>DeveloperSupportEmail</Name>
                <Text/>
                <Value></Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>SupportEmailButton</Name>
                <Text>Write an e-mail to support</Text>
                <EventId>EMAIL_TO_SUPPORT</EventId>
                <Value>8631</Value>
                <ValueType>PictureResourceButton</ValueType>
                <WidthInRow>5</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
          <Parameter>
            <Name>DeveloperHomepageRow</Name>
            <Text>Homepage</Text>
            <ValueType>Row</ValueType>
            <Visible>DeveloperHomepage</Visible>
            <Parameters>
              <Parameter>
                <Name>DeveloperHomepage</Name>
                <Text/>
                <Value></Value>
                <ValueType>Text</ValueType>
              </Parameter>
              <Parameter>
                <Name>HomepageButton</Name>
                <Text>Go to the homepage</Text>
                <EventId>GO_TO_HOMEPAGE</EventId>
                <Value>8631</Value>
                <ValueType>PictureResourceButton</ValueType>
                <WidthInRow>5</WidthInRow>
              </Parameter>
            </Parameters>
          </Parameter>
        </Parameters>
      </Parameter>
    </Parameters>
  </Page>

  <Page>
    <Name>__HiddenPage__</Name>
    <Text></Text>
    <Parameters>
      <Parameter>
        <Name>PluginStatus</Name>
        <Text />
        <Value>0</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
      <Parameter>
        <Name>PluginHasGitHub</Name>
        <Text />
        <Value>False</Value>
        <ValueType>CheckBox</ValueType>
      </Parameter>
      <Parameter>
        <Name>CurrentPaletteState</Name>
        <Text />
        <Value>2001</Value>
        <ValueType>Integer</ValueType>
      </Parameter>
    </Parameters>
  </Page>
</Element>